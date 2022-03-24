from flask import Blueprint, request
try:
    from keywordAnalysis.keywordExtraction import keywordExtractionMethods
    from middlewares import login_required
except ImportError:
    from apis.http.api.keywordAnalysis.keywordExtraction import keywordExtractionMethods
    from apis.http.api.middlewares import login_required
import json

keywords_api = Blueprint('keyword_analysis_api', __name__, template_folder='templates')


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


@keywords_api.route("/keywordAnalysis/availableMethods", methods=["GET"])
def list_avalable_methods():
    return json_response({'available_methods': ['rake',
                                                # 'keybert'
                                                ]})


@keywords_api.route("/keywordAnalysis/<string:methods>", methods=["POST"])
@login_required
def analyze_readability(methods):
    text = request.get_data().decode('utf-8', errors='ignore')
    if methods == "" or methods == 'all':
        analyze_methods = None
    else:
        analyze_methods = methods.split(',')

    keyphrase_range_str = request.args.get('keyphrase_range')
    if keyphrase_range_str is None:
        keyphrase_range = (1, 2)
    else:
        keyphrase_range = tuple(int(el) for el in keyphrase_range_str.split(' '))

    language = request.args.get('language')

    return json_response(keywordExtractionMethods.analyze_keywords(text, analyze_methods, keyphrase_range, language))