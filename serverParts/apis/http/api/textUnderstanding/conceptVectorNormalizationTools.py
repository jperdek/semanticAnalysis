import math
import json
from typing import Optional


class ConceptVectorNormalizationTools:

    @staticmethod
    def evaluate_vector_size(vector_values: list) -> float:
        sum_squares = 0.0
        for str_value in vector_values:
            value = float(str_value)
            sum_squares = sum_squares + value * value
        return math.sqrt(sum_squares)

    @staticmethod
    def save_values_for_kmedoid_concept_normalized(result_dict: dict, file_name: str, separator='\t', decimal_places=5):
        with open(file_name, "w", encoding="utf-8") as file:
            for context_key, context in result_dict.items():
                vector_position_values = ""
                vector_size = ConceptVectorNormalizationTools.evaluate_vector_size(context.values())
                for vector_position_name, vector_position_value in context.items():
                    vector_position_values = vector_position_values + separator \
                                             + vector_position_name + "(" + \
                                             str(round(float(vector_position_value)
                                                       / vector_size, decimal_places)) + ")"
                add_length = separator + str(len(context.keys()))
                # separator between them should be included in second variable
                file.write(context_key + vector_position_values + add_length + "\n")

    @staticmethod
    def save_values_for_kmedoid_concept_normalized_as_dict(result_dict: dict, file_name: str):
        normalized_values_dict = dict()
        for context_key, context in result_dict.items():
            normalized_values_dict[context_key] = dict()
            vector_size = ConceptVectorNormalizationTools.evaluate_vector_size(context.values())
            for vector_position_name, vector_position_value in context.items():
                normalized_values_dict[context_key][vector_position_name] = float(vector_position_value) / vector_size
        ConceptVectorNormalizationTools.save_as_json(normalized_values_dict, file_name)

    @staticmethod
    def get_value_for_concept(concept: str, type_word: str, normalized_values_dict: dict) -> float:
        # concept not exists
        if concept not in normalized_values_dict:
            return 0.0
        # type word not exists in concept
        if type_word not in normalized_values_dict[concept]:
            return 0.0

        return normalized_values_dict[concept][type_word]

    @staticmethod
    def evaluate_concept_cluster_vector_for_cluster_using_concept(concept: str,
                                                                  normalized_values_dict: dict,
                                                                  clusters: dict) -> Optional[dict]:
        if concept not in normalized_values_dict:
            return None
        result = dict()
        result_name = dict()
        concept_cluster_vector = dict()
        for typed_word in normalized_values_dict[concept].keys():
            if typed_word in clusters.values():
                cluster_name = clusters[typed_word]
                if result[cluster_name] is None:
                    result[cluster_name] = 0.0
                    result_name[cluster_name] = ""
                # sum normalized value for every cluster
                result[clusters[typed_word]] = result[cluster_name] + normalized_values_dict[
                    concept][typed_word]
                if result_name[cluster_name] == "":
                    result_name[cluster_name] = typed_word
                else:
                    result_name[cluster_name] = result_name[cluster_name] + typed_word
        for cluster_name, value in result.items():
            concept_cluster_vector[cluster_name] = value
        return dict(sorted(concept_cluster_vector.items(), key=lambda x: x[1]))

    @staticmethod
    def load_as_json(filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_as_json(object_to_save: dict, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(object_to_save, file)
