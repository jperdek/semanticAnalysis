import math
import json


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
    def load_as_json(filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_as_json(object_to_save: dict, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(object_to_save, file)
