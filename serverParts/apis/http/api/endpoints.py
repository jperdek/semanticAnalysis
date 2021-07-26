from senseAnalysis.categorization.senseTextProcess import SemcorAnalyser
from flask import Flask, json, g
import flask_cors
from senseAnalysis.senseAnalysisApi import sense_api, load_local_json_file
from readabilityAnalysis.readabilityAnalysisApi import readability_api
from segmentationAnalysis.segmentationAnalysisApi import segmentation_api
from keywordAnalysis.keywordAnalysisApi import keywords_api


app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

flask_cors.CORS(app)
app.register_blueprint(sense_api)
app.register_blueprint(readability_api)
app.register_blueprint(segmentation_api)
app.register_blueprint(keywords_api)


@app.before_first_request
def startup():
    print('Preparing for requests execution...')
    domain_parts = load_local_json_file('domain-parts.json')
    semcor_frequencies = load_local_json_file('semcor_frequencies.json')
    g.semcorAnalyser = SemcorAnalyser(domain_parts, semcor_frequencies, True)
    print('preparation completed successfully!')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)