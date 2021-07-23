import os

from senseAnalysis.categorization.senseTextProcess import SemcorAnalyser
from middlewares import login_required
from flask import Flask, json, g
import flask_cors
from senseAnalysis.senseAnalysisApi import simple_page, load_local_json_file


def do_something():
    print('progress')
    domain_parts = load_local_json_file('domain-parts.json')
    semcor_frequencies = load_local_json_file('semcor_frequencies.json')
    print('OK')
    g.semcorAnalyser = SemcorAnalyser(domain_parts, semcor_frequencies, True)
    print('end')


class MyFlaskApp(Flask):
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):

    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        do_something()
    super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = Flask(__name__, static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
flask_cors.CORS(app)
app.register_blueprint(simple_page)


@app.route("/kudos", methods=["GET"])
@login_required
def index():
    return json_response('Index works')


@app.route("/kudos", methods=["POST"])
@login_required
def create():
    return json_response({'Creation works'});


@app.route("/kudo/<int:repo_id>", methods=["DELETE"])
@login_required
def delete(repo_id):
    return json_response({'error': 'kudo not found'}, 404)


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


@app.before_first_request
def startup():
    print('startup')
    global semcorAnalyser
    print('progress')
    domain_parts = load_local_json_file('domain-parts.json')
    semcor_frequencies = load_local_json_file('semcor_frequencies.json')
    print('OK')
    g.semcorAnalyser = SemcorAnalyser(domain_parts,semcor_frequencies, True)
    print('end')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)