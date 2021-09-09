
class AffinityScore:

    @staticmethod
    def evaluate_value_for_cluster(concept: str, normalized_values_dict: dict, clusters: dict):
        if concept not in normalized_values_dict:
            return None
        result = dict()
        for typed_word in normalized_values_dict[concept]:
            if typed_word in clusters:
                if result[clusters[typed_word]] is None:
                    result[clusters[typed_word]] = 0.0
                # sum normalized value for every cluster
                result[clusters[typed_word]] = result[clusters[typed_word]] + normalized_values_dict[concept][
                    typed_word]
        return dict(sorted(result.items(), key=lambda x: x[1]))