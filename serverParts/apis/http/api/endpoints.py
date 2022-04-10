import sys
from flask import Flask, g
import flask_cors

from senseAnalysis.categorization.senseTextProcess import SemcorAnalyser
from senseAnalysis.senseAnalysisApi import sense_api, load_local_json_file
from readabilityAnalysis.readabilityAnalysisApi import readability_api
from segmentationAnalysis.segmentationAnalysisApi import segmentation_api
from keywordAnalysis.keywordAnalysisApi import keywords_api
from automatization.automatizationApi import automatization_api
from textUnderstanding import clustersFile
from textUnderstanding.affinity import AffinityHelper
from textUnderstanding.textUnderstandingApi import text_understanding_api, load_local_picle_file
from textUnderstanding.meaningAggregationApi import meaning_aggregation_api


app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

flask_cors.CORS(app)
# app.register_blueprint(sense_api, url_prefix="/api/senseAnalysis")
app.register_blueprint(sense_api, url_prefix="/")
app.register_blueprint(readability_api)
app.register_blueprint(segmentation_api)
app.register_blueprint(keywords_api)
app.register_blueprint(text_understanding_api)
app.register_blueprint(automatization_api)
app.register_blueprint(meaning_aggregation_api)


@app.before_first_request
def startup():
    print('Preparing for requests execution...')
    domain_parts = load_local_json_file('domain-parts.json')
    semcor_frequencies = load_local_json_file('semcor_frequencies.json')
    g.indexed_guesses = load_local_json_file('indexed-guesses.json')
    sample_normalized_values_dict = load_local_json_file('data-concept-instance-relations-remake-normalized.json')

    g.text_categories_svc_pickle = load_local_picle_file('linear_svc_text_categories.pickle')
    g.text_categories_tfidf_pickle = load_local_picle_file('tfidf_text_categories.pickle')
    g.affinity_helper = AffinityHelper(clustersFile.clusters, sample_normalized_values_dict)
    g.semcorAnalyser = SemcorAnalyser(domain_parts, semcor_frequencies, True)
    print('Preparation completed successfully!')


def launch():
    app.run(host="0.0.0.0", debug=False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "production":
        app.run(host="0.0.0.0", debug=False, port=8080)
    else:
        app.run(host="0.0.0.0", debug=True)
