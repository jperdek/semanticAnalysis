import json
import pickle
from flask import Blueprint, send_from_directory
from flask import g, request

from middlewares import login_required
from textUnderstanding.affinity import AffinityHelper
from textUnderstanding.guessedWord.conceptGuessWord import get_texts_from_range, count_tf_idf
from textUnderstanding import clustersFile

text_understanding_api = Blueprint('text_understanding_api', __name__, template_folder='templates')
categories_classification = {'Computer_Science': 0, 'Crime': 1, 'Science': 2,
                             'politics': 3, 'physics': 4, 'History': 5, 'accounts': 6,
                             'entertainment': 7, 'biology': 8, 'technologie': 9, 'medical': 10,
                             'Maths': 11, 'graphics': 12, 'historical': 13, 'business': 14,
                             'sport': 15, 'food': 16, 'geography': 17, 'space': 18}


def load_local_json_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return stream.get_json()


def load_local_picle_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return pickle.loads(stream.data)


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json'}


@text_understanding_api.route("/textUnderstanding/textUnderstandingMethods", methods=["GET"])
def list_avalable_methods():
    return json_response({'available_methods': ['categoryFinder', 'relatedTextFinder', 'clustersAnalyzer']})


affinity_helper = None
guess_words_file = None
text_categorie_pickle = None


@text_understanding_api.route("/textUnderstanding/clustersAnalyzer", methods=["POST"])
@login_required
def associate_clusters():
    global affinity_helper
    sample_text = request.get_data().decode('utf-8', errors='ignore')

    if affinity_helper is not None:
        g.affinity_helper = affinity_helper
    if 'affinity_helper' not in g:
        print("Loads for each request")
        sample_normalized_values_dict = load_local_json_file('data-concept-instance-relations-remake-normalized.json')
        affinity_helper = g.affinity_helper = AffinityHelper(clustersFile.clusters, sample_normalized_values_dict)
    else:
        affinity_helper = g.affinity_helper
    concept_cluster_vector, cluster_words = affinity_helper.get_concept_vector(sample_text)

    result = dict()
    result["result"] = concept_cluster_vector
    result["clusters_content"] = cluster_words
    return json_response(result)


@text_understanding_api.route("/textUnderstanding/categoryFinder", methods=["POST"])
@login_required
def classify_to_text_categories():
    global text_categorie_pickle
    sample_text = request.get_data().decode('utf-8', errors='ignore')

    if text_categorie_pickle is not None:
        g.text_categories_svc_pickle = text_categorie_pickle
    if 'affinity_helper' not in g:
        print("Loads for each request")
        linear_svc_text_categories = g.text_categories_svc_pickle = \
            load_local_picle_file('linear_svc_text_categories.pickle')
        g.text_categories_tfidf_pickle = tfidf_vectorizer = load_local_picle_file('tfidf_text_categories.pickle')
    else:
        linear_svc_text_categories = g.text_categories_svc_pickle
        tfidf_vectorizer = g.text_categories_tfidf_pickle

    tfidf_test = tfidf_vectorizer.transform([sample_text.lower()])
    result = linear_svc_text_categories.predict(tfidf_test)

    category = ""
    for category_name, value in categories_classification.items():
        if value == result[0]:
            category = category_name
            break
    return json_response({"category": category})


@text_understanding_api.route("/textUnderstanding/relatedTextFinder/<string:category>", methods=["POST"])
@login_required
def find_related_text(category):
    global guess_words_file
    sample_text = request.get_data().decode('utf-8', errors='ignore')

    if guess_words_file is not None:
        g.indexed_guesses = guess_words_file
    if 'guess_words_file' not in g:
        print("Loads for each request")
        guess_words_file = g.indexed_guesses = load_local_json_file('indexed-guesses.json')
    else:
        guess_words_file = g.indexed_guesses

    maximum = count_tf_idf(sample_text, guess_words_file, category)
    results = get_texts_from_range(sample_text, guess_words_file, category, maximum)
    return json_response(results)
