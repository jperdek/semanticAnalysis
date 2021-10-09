from typing import Optional

import numpy as np
import math
import json

from serverParts.apis.http.api.textUnderstanding.textPreprocessing import POSTagging


class AffinityScore:

    @staticmethod
    def evaluate_affinity_score(similarity: float, coherence: float) -> float:
        return max(similarity, coherence)

    @staticmethod
    def evaluate_similarity_between_typed_terms(typed_term1: str,
                                                typed_term2: str,
                                                normalized_values_dict: dict,
                                                clusters: dict) -> float:
        concept_cluster_x = AffinityScore.evaluate_concept_cluster_vector_for_cluster_using_concept(
            typed_term1, normalized_values_dict, clusters)
        concept_cluster_y = AffinityScore.evaluate_concept_cluster_vector_for_cluster_using_concept(
            typed_term2, normalized_values_dict, clusters)
        if concept_cluster_x is None or concept_cluster_y is None:
            return 0.0
        return AffinityScore.evaluate_cosine_weight(concept_cluster_x, concept_cluster_y)

    @staticmethod
    def evaluate_coherence_between_typed_terms(
            typed_term1: str, typed_term2: str,
            normalized_values_dict: dict, clusters: dict) -> float:
        pos_tagging = POSTagging()
        word, pos = pos_tagging.pos_of_word(typed_term1)
        concept_cluster_y = AffinityScore.evaluate_concept_cluster_vector_for_cluster_using_concept(
            typed_term2, normalized_values_dict, clusters)
        if pos != 'n':  # for verbs adjectives and attribute w(typed_term1, concept_cluster)
            coherence_concept_cluster = normalized_values_dict[typed_term1]  # direct association
            return AffinityScore.evaluate_cosine_weight(coherence_concept_cluster, concept_cluster_y)
        else:
            whole_coherence_value = 0.0
            #coherence_concept_cluster = normalized_values_dict[typed_term1]  # direct association
            print(normalized_values_dict)
            concept_cluster_vectors = AffinityScore.evaluate_concept_cluster_vector_for_cluster_using_concept(
                typed_term1, normalized_values_dict, clusters)
            word_cluster = clusters[typed_term1]
            for cluster_name, value in concept_cluster_vectors.items():
                edge_value = AffinityScore.evaluate_edge_between_clusters(
                    cluster_name, word_cluster, normalized_values_dict, clusters)
                whole_coherence_value = whole_coherence_value + value * edge_value
            if concept_cluster_y is None:
                return 0.0
            return AffinityScore.evaluate_cosine_weight(concept_cluster_vectors, concept_cluster_y)

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
                if cluster_name not in result:
                    result[cluster_name] = 0.0
                    result_name[cluster_name] = ""
                # sum normalized value for every cluster
                result[cluster_name] = result[cluster_name] + normalized_values_dict[
                    concept][typed_word]
                if result_name[cluster_name] == "":
                    result_name[cluster_name] = typed_word
                else:
                    result_name[cluster_name] = result_name[cluster_name] + typed_word
        for cluster_name, value in result.items():
            concept_cluster_vector[cluster_name] = value
        return dict(sorted(concept_cluster_vector.items(), key=lambda x: x[1]))

    @staticmethod
    def evaluate_edge_between_clusters(cluster1: str, cluster2: str,
                                       normalized_values_dict: dict, clusters: dict):
        cluster_data1 = dict()
        cluster_data2 = dict()
        for word_name, cluster in clusters.items():
            if cluster == cluster1:
                if word_name in normalized_values_dict:
                    print(word_name)
                    for key, value in normalized_values_dict[word_name].items():
                        cluster_data1[key] = value
            if cluster == cluster2:
                if word_name in normalized_values_dict:
                    print(word_name)
                    for key, value in normalized_values_dict[word_name].items():
                        cluster_data2[key] = value
        return AffinityScore.evaluate_cosine_weight(cluster_data1, cluster_data2)

    @staticmethod
    def load_json(file: str):
        with open(file, encoding='utf-8') as file_path:
            return json.load(file_path)

    @staticmethod
    def process_clusters(clusters: dict):
        processed = dict()
        for cluster_name, cluster_data in clusters.items():
            for cluster_data_name in cluster_data:
                processed[cluster_data_name] = cluster_name
        return processed


if __name__ == '__main__':
    given_typed_term1 = 'law'
    given_typed_term2 = 'study'
    sample_clusters = AffinityScore.load_json('group.json')
    processed_clusters = AffinityScore.process_clusters(sample_clusters)
    sample_normalized_values_dict = AffinityScore.load_json('data-concept-instance-relations-remake-normalized.json')
    similarity = AffinityScore.evaluate_similarity_between_typed_terms(given_typed_term1, given_typed_term2,
                                                                       sample_normalized_values_dict, processed_clusters)
    coherence = AffinityScore.evaluate_coherence_between_typed_terms(given_typed_term1, given_typed_term2,
                                                                     sample_normalized_values_dict, processed_clusters)
    affinity = AffinityScore.evaluate_affinity_score(similarity, coherence)
    print(affinity)
