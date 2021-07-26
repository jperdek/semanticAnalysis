from flask import Blueprint, request, send_from_directory
import json
from segmentationAnalysis.pageAnalyser import cetdExtractor
from segmentationAnalysis.pageAnalyser import textExtractor
from segmentationAnalysis.pageAnalyser import SOMExtractor
from serverParts.apis.http.api.middlewares import login_required
import uuid


def load_local_json_file(file_name):
    stream = send_from_directory('web/static', file_name)
    stream.direct_passthrough = False
    return stream.get_json()


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json' }


segmentation_api = Blueprint('segmentation_api', __name__, template_folder='templates')


@segmentation_api.route("/segmentationAnalysis/CETD/availableMethods", methods=["GET"])
def list_avalable_methods():
    return json_response({'available_methods':
                              ['normal', 'edgare', 'variant']})


@segmentation_api.route("/segmentationAnalysis/CETD/<string:methods>", methods=["POST"])
@login_required
def cetd_segmentation(methods):
    html_page = request.get_data().decode('utf-8', errors='ignore')
    if methods == "" or methods == 'all':
        analyze_methods = None
    else:
        analyze_methods = methods.split(',')

    return json_response(cetdExtractor.apply_segmentation(html_page, analyze_methods))


@segmentation_api.route("/segmentationAnalysis/text", methods=["POST"])
@login_required
def text_segmentation():
    html_page = request.get_data().decode('utf-8', errors='ignore')
    category = request.args.get('category')

    return json_response(textExtractor.convert_document_to_text(html_page, category))


def check_and_add_error(response, page_tree, page_name):
    if 'errors' not in page_tree:
        page_tree['errors'] = []
    page_tree['errors'].append({
        "page_name": page_name,
        "error": response
    })
    print(response)


@segmentation_api.route("/segmentationAnalysis/SOM/createTree", methods=["POST"])
@login_required
def create_som_three():
    html_pages = request.get_data().decode('utf-8', errors='ignore').\
        split('<----------DIVISION_OF_MANY_PAGES----------->')
    page_names = request.args.get('names')
    if page_names is not None:
        page_names = page_names.split(',')
    som_tree = dict()

    for index, html_page in enumerate(html_pages):
        if page_names is None or index not in page_names:
            page_name = str(uuid.uuid4())
        else:
            page_name = page_names[index]

        response = SOMExtractor.SOMBeautifulSoup.parse_tree_beautiful_soup(html_page, page_name=page_name,
                                                                                         root=som_tree)
        if str(response).startswith('Error:'):
            check_and_add_error(response, page_tree, page_name)
        else:
            som_tree = response
            if 'whole_count' not in som_tree:
                som_tree['whole_count'] = 1
            else:
                som_tree['whole_count'] = som_tree['whole_count'] + 1
    return json_response(som_tree)


@segmentation_api.route("/segmentationAnalysis/SOM/updateTree", methods=["POST"])
@login_required
def update_som_three():
    pages_and_tree = request.get_data().decode('utf-8', errors='ignore').\
        split('<----------DIVISION_OF_MANY_PAGES_AND_SOM_THREE----------->')
    html_pages = pages_and_tree[not -1].split('<----------DIVISION_OF_MANY_PAGES----------->')
    som_tree = json.loads(pages_and_tree[-1])  # obtaining SOM tree
    page_names = request.args.get('names')     # get names for files if are specified
    if page_names is not None:
        page_names = page_names.split(',')

    for index, html_page in enumerate(html_pages):
        if page_names is None or index not in page_names:
            page_name = str(uuid.uuid4())
        else:
            page_name = page_names[index]

        response = SOMExtractor.SOMBeautifulSoup.parse_tree_beautiful_soup(html_page, page_name=page_name, root=som_tree
                                                                           )
        if str(response).startswith('Error:'):
            check_and_add_error(response, som_tree, page_name)
        else:
            som_tree = response
            if 'whole_count' not in som_tree:
                som_tree['whole_count'] = 1
            else:
                som_tree['whole_count'] = som_tree['whole_count'] + 1

    return json_response(som_tree)


@segmentation_api.route("/segmentationAnalysis/SOM/extractFromTree", methods=["POST"])
@login_required
def extract_from_som_three():
    domain_som_tree = request.get_json()
    accept_percentage = request.args.get('accept_percentage')
    if accept_percentage is None:
        accept_percentage = 0.2
    else:
        accept_percentage = float(accept_percentage)

    category = request.args.get('category')
    if category is None:
        category = "unkn"

    extracted_data = dict()
    SOMExtractor.ExtractFromTree.extract_info_from_domain(domain_som_tree, accept_percentage, extracted_data, category,
                                                          add_domain=False, domain_name="")
    return json_response(extracted_data)