import os
import json
from typing import Optional, Union

from bs4 import BeautifulSoup
from flask import send_from_directory

from serverParts.apis.http.api.segmentationAnalysis.pageAnalyser.SOMExtractor import SOMBeautifulSoup


def verify_html(text):
    processed_html = BeautifulSoup(text, "html.parser")
    if processed_html.find() is None:
        return False
    else:
        return True


class SOMTools:
    @staticmethod
    def analyze_SOM_tree(
            domain_json: dict, file_content: dict, page_file_path: Optional[str],
            file_name: str, domain_name: str, category: str,
            analyzed_trees: dict = None, file_tree_soup: BeautifulSoup = None,
            evaluate_validity: bool = False) -> (Optional[bool], dict):
        if category not in file_content:
            file_content[category] = dict()
        if domain_name not in file_content[category]:
            file_content[category][domain_name] = dict()
        if file_name not in file_content[category][domain_name]:
            file_content[category][domain_name][file_name] = dict()
        file_content[category][domain_name][file_name]["whole_count"] = domain_json['whole_count']
        file_content[category][domain_name][file_name]["count"] = 0

        analyzed_trees_domain = None
        candidate_json_tree = dict()
        if page_file_path:
            file_tree_soup = SOMBeautifulSoup.create_dom_beautiful_soup(page_file_path.replace("\\", "/"))

        SOMBeautifulSoup.parse_tree_dom_beautiful_soup(candidate_json_tree, file_tree_soup, 1, file_name)
        if analyzed_trees:
            analyzed_trees_domain = analyzed_trees[category][domain_name]

        SOMTools.parse_tree_extract(domain_json, candidate_json_tree,
                                    file_content[category][domain_name], file_name, analyzed_trees_domain)
        if evaluate_validity:
            if file_content[category][domain_name][file_name]["count"] > analyzed_trees_domain["domain_average"]:
                return True, candidate_json_tree
            return False, candidate_json_tree
        return None, candidate_json_tree

    @staticmethod
    def parse_tree_extract(domain_tree_json: dict, file_json_tree: dict,
                           file_content: dict, file_name: str, analyzed_trees_domain: dict = None):
        for name_domain_tree, content_domain_tree in domain_tree_json.items():
            for name_file_tree, content_file_tree in file_json_tree.items():
                if analyzed_trees_domain and analyzed_trees_domain["domain_average"] \
                        < file_content[file_name]["count"]:
                    return
                if name_file_tree == name_domain_tree and isinstance(content_domain_tree, dict):
                    if 'flag' in content_domain_tree and content_domain_tree['flag']:
                        file_content[file_name]["count"] = \
                            file_content[file_name]["count"] + content_domain_tree["count"]
                        if analyzed_trees_domain and analyzed_trees_domain["domain_average"] \
                                < file_content[file_name]["count"]:
                            return
                    SOMTools.parse_tree_extract(content_domain_tree, content_file_tree,
                                                file_content, file_name, analyzed_trees_domain)

    @staticmethod
    def load_local_json_file(file_name):
        stream = send_from_directory('web/static', file_name)
        stream.direct_passthrough = False
        return stream.get_json()

    @staticmethod
    def analyze_som_comparisons(html_file: str, analysis_dict_file_path: str = "som_ranges.json",
                                only_one_domain: bool = True,
                                som_files: list = ["nbaplayer-foxsports(425).json", "nbaplayer-msnca(434).json",
                                                   "nbaplayer-si(515).json"]) \
            -> (Optional[str], dict, Optional[dict]):
        analysis_results = SOMTools.load_local_json_file(analysis_dict_file_path)
        candidate_results = dict()
        candidate_file_name = "analyzed_file"
        for som_file_name in som_files:
            path_to_json_tree = "somExamples/trees/" + som_file_name
            domain_json_tree = SOMTools.load_local_json_file(path_to_json_tree)

            category_name, domain_name = som_file_name[:som_file_name.find('.json')].split('-')
            domain_match, candidate_tree = SOMTools.analyze_SOM_tree(
                domain_json_tree, candidate_results, None, candidate_file_name,
                domain_name, category_name, analyzed_trees=analysis_results,
                file_tree_soup=BeautifulSoup(html_file, "html.parser"), evaluate_validity=True)
            if only_one_domain and domain_match:
                return path_to_json_tree, domain_json_tree, candidate_tree
        return None, candidate_results, None

    @staticmethod
    def get_unique_content_from_list(content_list: list, unique_content: dict, clear_spaces: bool = False) -> None:
        for content_string in content_list:
            analyzed_text = content_string.strip()
            if clear_spaces:
                analyzed_text = ' '.join(analyzed_text.split())
            unique_content[analyzed_text] = ""

    @staticmethod
    def concatenate_list_content(extracted_data: list, clear_spaces=True) -> str:
        unique_content = dict()
        SOMTools.get_unique_content_from_list(extracted_data, unique_content, clear_spaces=clear_spaces)
        return " ".join(unique_content.keys())

    @staticmethod
    def extract_unique_strings(extracted_data: dict, clear_spaces: bool = False) -> list:
        unique_content = dict()
        for file_name, file_content in extracted_data.items():
            for content_name, content in file_content.items():
                if content_name == "text":
                    SOMTools.get_unique_content_from_list(content, unique_content, clear_spaces)
        return list(unique_content.keys())


class OfflineSOMTools:
    @staticmethod
    def load_as_json(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_as_json(object_to_save, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(object_to_save, file)

    @staticmethod
    def load_som_trees(path_to_trees: str = os.getcwd()[:os.getcwd().rfind('\\')] + '/web/static/somExamples',
                       number_samples: int = 5,
                       file_format: str = "{category_name}-{sample_index}-{domain_name}.htm",
                       candidates_comparisons: bool = True,
                       save_as_json: bool = True,
                       saved_json_path: str = "som_comparison_counts.json") -> dict:
        path_to_trees_dict = os.path.join(path_to_trees, "trees")
        path_to_candidates = os.path.join(path_to_trees, "candidate")
        candidate_results = dict()
        for json_tree_name in os.listdir(path_to_trees_dict):
            json_tree_location = os.path.join(path_to_trees_dict, json_tree_name)
            domain_json_tree = OfflineSOMTools.load_as_json(json_tree_location)
            category_name, domain_name = json_tree_name[:json_tree_name.find('.json')].split('-')

            print("Started processing JSON tree: " + domain_name)
            if candidates_comparisons:
                print("Analysis for every file  ...long execution!")

            for index in range(1, number_samples + 1):
                if candidates_comparisons:
                    for candidate_file_name in os.listdir(path_to_candidates):
                        path_to_candidate = os.path.join(path_to_candidates, candidate_file_name)
                        SOMTools.analyze_SOM_tree(
                            domain_json_tree, candidate_results, path_to_candidate,
                            candidate_file_name, domain_name, category_name)
                else:
                    candidate_file_name = file_format.format(category_name=category_name, sample_index=str(index),
                                                             domain_name=domain_name)
                    path_to_candidate = os.path.join(path_to_candidates, candidate_file_name)
                    SOMTools.analyze_SOM_tree(
                        domain_json_tree, candidate_results, path_to_candidate,
                        candidate_file_name, domain_name, category_name)
        if save_as_json:
            OfflineSOMTools.save_as_json(candidate_results, saved_json_path)
        return candidate_results

    @staticmethod
    def prepare_domain_dict():
        return {
            "domain_samples": 0,
            "domain_count": 0,
            "other_domain_samples": 0,
            "other_domain_count": 0,
        }

    @staticmethod
    def analyze_som_comparisons(analysis_dict: dict, toleration: float = 0.5) -> dict:
        category_results = dict()
        for category_name, category_content in analysis_dict.items():
            category_results[category_name] = dict()
            for domain_name, domain_content in category_content.items():
                domain_results = OfflineSOMTools.prepare_domain_dict()

                for tree_name, tree_info in domain_content.items():
                    if domain_name in tree_name:
                        domain_results["domain_samples"] = domain_results["domain_samples"] + 1
                        domain_results["domain_count"] = domain_results["domain_count"] + tree_info["count"]
                    else:
                        domain_results["other_domain_samples"] = domain_results["other_domain_samples"] + 1
                        domain_results["other_domain_count"] = domain_results["other_domain_count"] + tree_info["count"]

                domain_results["domain_average"] = \
                    domain_results["domain_count"] / (0.0 + domain_results["domain_samples"])
                domain_results["other_domain_average"] = \
                    domain_results["other_domain_count"] / (0.0 + domain_results["other_domain_samples"])

                domain_results["allowed_count"] = domain_results["other_domain_samples"] \
                                                  + (domain_results["domain_average"] -
                                                     domain_results["other_domain_samples"]) * (1.0 - toleration)
                category_results[category_name][domain_name] = domain_results
        return category_results


if __name__ == "__main__":
    analysis_results = OfflineSOMTools.load_som_trees(saved_json_path="som_comparison_counts.json")
    # analysis_results = OfflineSOMTools.load_as_json("som_comparison_counts.json")
    analyzed_results = OfflineSOMTools.analyze_som_comparisons(analysis_results)
    OfflineSOMTools.save_as_json(analyzed_results, "som_ranges.json")

