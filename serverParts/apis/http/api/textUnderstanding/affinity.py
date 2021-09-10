from serverParts.apis.http.api.textUnderstanding.conceptVectorNormalizationTools import ConceptVectorNormalizationTools
import numpy as np
import math


class AffinityScore:

    @staticmethod
    def evaluate_affinity_score(similarity: float, coherence: float) -> float:
        return max(similarity, coherence)

    @staticmethod
    def evaluate_similarity_between_typed_terms(typed_term1: str,
                                                typed_term2: str,
                                                normalized_values_dict: dict,
                                                clusters: dict) -> float:
        concept_cluster_x = ConceptVectorNormalizationTools.evaluate_concept_cluster_vector_for_cluster_using_concept(
            typed_term1, normalized_values_dict, clusters)
        concept_cluster_y = ConceptVectorNormalizationTools.evaluate_concept_cluster_vector_for_cluster_using_concept(
            typed_term2, normalized_values_dict, clusters)
        return AffinityScore.evaluate_cosine_weight(concept_cluster_x, concept_cluster_y)

    @staticmethod
    def evaluate_coherence_between_typed_terms(typed_term1: str, typed_term2: str) -> float:
        return 0.0

    @staticmethod
    def evaluate_cosine_weight(dict_vector1, dict_vector2) -> float:
        unique_keys = np.unique(list(dict_vector1.keys()) + list(dict_vector2.keys()))
        upper_value = 0.0
        bottom_value_vector1 = 0.0
        bottom_value_vector2 = 0.0
        for key in unique_keys:
            if key in dict_vector1 and key in dict_vector2:  # in other cases result will be zero
                upper_value = upper_value + float(dict_vector1[key]) * float(dict_vector2[key])
            if key in dict_vector1:  # in other cases added value will be zero
                bottom_value_vector1 = bottom_value_vector1 + pow(float(dict_vector1[key]), 2.0)
            if key in dict_vector2:  # in other cases added value will be zero
                bottom_value_vector2 = bottom_value_vector2 + pow(float(dict_vector2[key]), 2.0)

        bottom_value_vector1 = math.sqrt(bottom_value_vector1)
        bottom_value_vector2 = math.sqrt(bottom_value_vector2)
        return upper_value / (0.0 + bottom_value_vector1 * bottom_value_vector2)