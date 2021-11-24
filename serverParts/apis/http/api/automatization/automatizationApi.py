from flask import Blueprint, g, request, send_from_directory
import json

from middlewares import login_required

from serverParts.apis.http.api.automatization.automatization_tools import verify_html, SOMTools
from serverParts.apis.http.api.segmentationAnalysis.pageAnalyser import cetdExtractor
from serverParts.apis.http.api.textUnderstanding.guessedWord.conceptGuessWord import count_tf_idf, get_texts_from_range
from serverParts.apis.http.api.textUnderstanding.textUnderstandingApi import categories_classification, \
    load_local_picle_file, load_local_json_file

automatization_api = Blueprint('automatization_api', __name__, template_folder='templates')


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


def load_local_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return stream.get_data().decode('utf-8', 'ignore')


@automatization_api.route("/automatization", methods=["POST"])
@login_required
def automatic_analysis():
    text = request.get_data().decode('utf-8', 'ignore')

    if verify_html(text):
        text = str(request.get_data())  # for text data it must be not loaded as binary data
        res = SOMTools.analyze_som_comparisons(text)
        result_text = cetdExtractor.apply_segmentation(text, ["normal"])["normal"]
        if result_text[0:6] != 'Error:':
            text = result_text

    if 'text_categories_svc_pickle' not in g or 'text_categories_tfidf_pickle' not in g:
        g.text_categories_svc_pickle = load_local_picle_file('linear_svc_text_categories.pickle')
        g.text_categories_tfidf_pickle = load_local_picle_file('tfidf_text_categories.pickle')
        g.indexed_guesses = load_local_json_file('indexed-guesses.json')

    tfidf_test = g.text_categories_tfidf_pickle.transform([text.lower()])
    result = g.text_categories_svc_pickle.predict(tfidf_test)

    print(verify_html(text))
    print(result)
    category = ""
    for category_name, value in categories_classification.items():
        if value == result[0]:
            category = category_name
            break

    category = category.lower()
    maximum = count_tf_idf(text, g.indexed_guesses, category)
    results = get_texts_from_range(text, g.indexed_guesses, category, maximum)

    return json_response({"category": category, "results": results})