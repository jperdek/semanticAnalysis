from flask import Blueprint, g, request, send_from_directory
import json
from neo4j.exceptions import ServiceUnavailable

from textUnderstanding.meaningAggregationApi import select_appropriate_aggregation_methods
from middlewares import login_required
from automatization.automatization_tools import verify_html, SOMTools
from segmentationAnalysis.pageAnalyser import cetdExtractor, SOMExtractor
from textUnderstanding.guessedWord.conceptGuessWord import count_tf_idf, get_texts_from_range, \
    get_texts_from_range_html_marks
from textUnderstanding.textUnderstandingApi import categories_classification, \
    load_local_picle_file, load_local_json_file
from senseAnalysis.senseAnalysisApi import apply_sense_analysis
from textUnderstanding.textUnderstandingApi import evaluate_concept_cluster_vector_and_cluster_words
from database_management.init_database_drivers import CoOccurrenceNetworkManager


automatization_api = Blueprint('automatization_api', __name__, template_folder='templates')


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


def load_local_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return stream.get_data().decode('utf-8', 'ignore')


co_occurrence_network_manager1 = None


@automatization_api.before_app_first_request
def startup_db_inicializations():
    global co_occurrence_network_manager1
    print('Preparing for automatization requests execution...')
    try:
        print("Trying to connect to neo4j co-occurrence network....")
        co_occurrence_network_manager1 = g.co_occurrence_network_manager = CoOccurrenceNetworkManager()
        g.co_occurrence_network_manager.initialize_additional_indexes()
        print("Connected!")
    except ServiceUnavailable or ConnectionRefusedError:
        print("Connecting to neo4j co-occurrence network failed. This functionality will not be available.")
        co_occurrence_network_manager1 = g.co_occurrence_network_manager1 = None
        pass
    print('Preparation for automatization completed successfully!')


def analyze_using_co_occurrence_network(text: str, result_response_data: dict):
    print("Getting aggregations")
    methods_to_use = ["all"]
    if "use_full_text" in request.headers:
        use_full_text = request.headers.get("use_full_text").lower() == "true"
    else:
        use_full_text = False
    try:
        result_response_data["co_occurrence_aggregations"] = \
            select_appropriate_aggregation_methods(text, methods_to_use,
                                                   co_occurrence_network_manager1, use_full_text)
    except Exception as e:
        result_response_data["co_occurrence_aggregations"] = None
        print(e)


@automatization_api.route("/automatization", methods=["POST"])
@login_required
def automatic_analysis():
    text = request.get_data().decode('utf-8', 'ignore')
    if "fast" in request.headers:
        fast = request.headers.get("fast").lower() == "true"
    else:
        fast = False
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
            result_response_data["analyzed_text"] = text = SOMTools.concatenate_list_content(extracted_data["text"],
                                                                                             clear_spaces=True)
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

    concept_cluster_array, cluster_words = evaluate_concept_cluster_vector_and_cluster_words(text, True)
    result_response_data["mappings"] = cluster_words
    result_response_data["concepts_with_scores"] = concept_cluster_array

    if not fast and co_occurrence_network_manager1:
        analyze_using_co_occurrence_network(text, result_response_data)
    else:
        result_response_data["co_occurrence_aggregations"] = None

    return json_response(result_response_data)
