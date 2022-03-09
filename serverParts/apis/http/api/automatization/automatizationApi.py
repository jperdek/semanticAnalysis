from flask import Blueprint, g, request, send_from_directory
import json

from middlewares import login_required

from automatization.automatization_tools import verify_html, SOMTools
from segmentationAnalysis.pageAnalyser import cetdExtractor, SOMExtractor
from textUnderstanding.guessedWord.conceptGuessWord import count_tf_idf, get_texts_from_range, get_texts_from_range_html_marks
from textUnderstanding.textUnderstandingApi import categories_classification, \
    load_local_picle_file, load_local_json_file
from senseAnalysis.senseAnalysisApi import apply_sense_analysis


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
    if "use_html_tags" in request.headers:
        use_html_tags = request.headers.get("use_html_tags").lower() == "true"
    else:
        use_html_tags = None
    result_response_data = dict()
    result_response_data["fileName"] = request.args.get("fileName")

    if verify_html(text):
        som_text = str(request.get_data())  # for text data it must be not loaded as binary data
        som_tree_path, domain_som_tree_or_statistics, candidate_tree = SOMTools.analyze_som_comparisons(som_text)
        if som_tree_path:
            extracted_data = dict()
            print("Identified SOM tree: " + som_tree_path)
            SOMExtractor.ExtractFromFile.extract_info_from_domain(
                domain_som_tree_or_statistics, 0.5, candidate_tree, extracted_data)
            result_response_data["analyzed_text"] = text = SOMTools.concatenate_list_content(extracted_data["text"], clear_spaces=True)
            result_response_data["category"] = som_tree_path

            return json_response(result_response_data)
        else:
            print("Som tree has not been identified. Printing statistics:")
            print(domain_som_tree_or_statistics)
            text = som_text

    result_text = cetdExtractor.apply_segmentation(text, ["normal"])["normal"]
    if result_text[0:6] != 'Error:':
        text = " ".join(result_text.replace("\\r", " ").replace("\\n", " ").replace("\\t", " ").split())

    if 'text_categories_svc_pickle' not in g or 'text_categories_tfidf_pickle' not in g:
        g.text_categories_svc_pickle = load_local_picle_file('linear_svc_text_categories.pickle')
        g.text_categories_tfidf_pickle = load_local_picle_file('tfidf_text_categories.pickle')
        g.indexed_guesses = load_local_json_file('indexed-guesses.json')

    tfidf_test = g.text_categories_tfidf_pickle.transform([text.lower()])
    result = g.text_categories_svc_pickle.predict(tfidf_test)

    category = ""
    result_response_data["categories_with_scores"] = apply_sense_analysis(text, k=8)["results"]
    for category_name, value in categories_classification.items():
        if value == result[0]:
            category = category_name
            continue

    category = category.lower()
    maximum = count_tf_idf(text, g.indexed_guesses, category)
    result_response_data["category"] = category

    if not use_html_tags:
        result_response_data["interesting_parts"] = get_texts_from_range(
            text, g.indexed_guesses, category, maximum, merge=True)
    else:
        result_response_data["analyzed_text"] = " ".join(get_texts_from_range_html_marks(
            text, g.indexed_guesses, category, maximum))

    return json_response(result_response_data)
