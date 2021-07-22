import os
import requests
from flask import Blueprint, request, send_from_directory, send_file
import json
from categorization.senseTextProcess import SemcorAnalyser
from flask import current_app
from flask import g


def load_local_json_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return stream.get_json()


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


simple_page = Blueprint('simple_page', __name__, template_folder='templates')

semcorAnalyser = None


@simple_page.route("/kudoss", methods=["GET"])
def analyze():
    global semcorAnalyser
    if semcorAnalyser is not None:
        g.semcorAnalyser = semcorAnalyser
    if 'semcorAnalyser' not in g:
        print("Loads for each request")
        domain_parts = load_local_json_file('domain-parts.json')
        semcor_frequencies = load_local_json_file('semcor_frequencies.json')
        g.semcorAnalyser = SemcorAnalyser(domain_parts, semcor_frequencies, True)
    else:
        semcorAnalyser = g.semcorAnalyser

    text = request.args.get('text')
    k = int(request.args.get('k'))
    result = g.semcorAnalyser.analyse_text_semcor(text, k)
    print(result)
    return json_response('Sense analyzis works')