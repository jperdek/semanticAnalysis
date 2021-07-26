from flask import Blueprint, g, request
from readabilityAnalysis.readability.readabilityAnalysis import ReadabilityAnalyser
import json

from middlewares import login_required

readability_api = Blueprint('readability_api', __name__, template_folder='templates')


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


@readability_api.route("/readabilityAnalysis/availableMethods", methods=["GET"])
def list_avalable_methods():
    return json_response({'available_methods':
                              ['flesch_kincaid', 'flesch_ease', 'dale_chall', 'ari', 'cli', 'gunning_fog',
                               'smog_all', 'smog', 'spache', 'linsear_write']})


@readability_api.route("/readabilityAnalysis/<string:methods>", methods=["GET"])
@login_required
def analyze_readability(methods):
    text = request.args.get('text')
    if methods == "" or methods == 'all':
        analyze_methods = None
    else:
        analyze_methods = methods.split(',')

    readability_analyzer = ReadabilityAnalyser(text)
    return json_response(readability_analyzer.check_readability(analyze_methods))


