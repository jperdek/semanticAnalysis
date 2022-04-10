from flask import Blueprint
from flask import g, request
import json
from neo4j.exceptions import ServiceUnavailable
from middlewares import login_required
from graphProcessing.network_manager import NetworkManager
from database_management.init_database_drivers import CoOccurrenceNetworkManager
from graphProcessing.co_occurrence_networks.meaning_analysis import \
    get_concepts_with_aggregated_meanings, get_meanings_with_aggregated_concepts
    
meaning_aggregation_api = Blueprint('meaning_aggregation_api', __name__, template_folder='templates')


@meaning_aggregation_api.route("/textUnderstanding/meaningAggregationMethods", methods=["GET"])
def list_available_methods():
    return json_response({"available_methods": ["concepts_with_aggregated_meanings",
                                                "meanings_with_aggregated_concepts"]})


def json_response(payload, status=200):
    return json.dumps(payload), status, {'content-type': 'application/json'}


co_occurrence_network_manager = None


def select_appropriate_aggregation_methods(sample_text: str, methods_to_use: list,
                                           co_occurrence_manager: NetworkManager,
                                           use_full_text: bool = True) -> dict:
    if "all" in str(methods_to_use):
        methods_to_use = ["concepts_with_aggregated_meanings", "meanings_with_aggregated_concepts"]

    results = dict()
    if len(methods_to_use) == 0:
        results["errors"].append("No method is specified")
    for method_name in methods_to_use:
        if method_name in "concepts_with_aggregated_meanings":
            print("Processing concepts with aggregated meanings...")
            results["concepts_with_aggregated_meanings"] = get_concepts_with_aggregated_meanings(
                sample_text, co_occurrence_manager, use_full_text)
        elif method_name in "meanings_with_aggregated_concepts":
            print("Processing meanings with aggregated concepts...")
            results["meanings_with_aggregated_concepts"] = get_meanings_with_aggregated_concepts(
                sample_text, co_occurrence_manager, use_full_text)
        else:
            if "errors" not in results:
                results["errors"] = list()
            results["errors"].append("Method " + method_name + " not found!")
    return results


@meaning_aggregation_api.route("/textUnderstanding/meaningAggregation", methods=["POST"])
@login_required
def aggregate_meaning_using_co_ocurrence():
    global co_occurrence_network_manager
    sample_text = request.get_data().decode('utf-8', errors='ignore')

    if co_occurrence_network_manager is not None:
        g.co_occurrence_network_manager = co_occurrence_network_manager
    if 'co_occurrence_network_manager' not in g:
        print("Loads for each request")
        try:
            co_occurrence_network_manager = g.co_occurrence_network_manager = CoOccurrenceNetworkManager()
            co_occurrence_network_manager.initialize_additional_indexes()
        except ServiceUnavailable or ConnectionRefusedError:
            return json_response({"error": "Connection can't be created. Database is probably down!"})
    else:
        co_occurrence_network_manager = g.co_occurrence_network_manager

    use_full_text = request.headers.get("use_full_text")
    methods_to_use = request.args.get("methods").split(',')
    results = select_appropriate_aggregation_methods(sample_text, methods_to_use,
                                                     co_occurrence_network_manager, use_full_text)
    return json_response(results)
