from flask import Blueprint, request, send_from_directory
import json
from senseAnalysis.categorization.senseTextProcess import SemcorAnalyser
from flask import g
from middlewares import login_required


def load_local_json_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return stream.get_json()


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


sense_api = Blueprint('sense_api', __name__, template_folder='templates')

semcorAnalyser = None


def apply_sense_analysis(text: str, k: int):
    global semcorAnalyser
    if semcorAnalyser is not None:
        g.semcorAnalyser = semcorAnalyser
    if 'semcorAnalyser' not in g:
        print("Loads for each request")
        domain_parts = load_local_json_file('domain-parts.json')
        semcor_frequencies = load_local_json_file('semcor_frequencies.json')
        semcorAnalyser = g.semcorAnalyser = SemcorAnalyser(domain_parts, semcor_frequencies, True)
    else:
        semcorAnalyser = g.semcorAnalyser

    return g.semcorAnalyser.analyse_text_semcor_results(text, k, return_results=True)


@sense_api.route("/api/senseAnalysis", methods=["GET"])
@login_required
def sense_analysis_get():
    text = request.args.get('text')
    k = int(request.args.get('k'))
    result = apply_sense_analysis(text, k)
    return json_response(result)


@sense_api.route("/api/senseAnalysis", methods=["POST"])
@login_required
def sense_analysis_post():
    text = request.get_data().decode('utf-8', "ignore")
    k = int(request.args.get('k'))
    result = apply_sense_analysis(text, k)
    return json_response(result)