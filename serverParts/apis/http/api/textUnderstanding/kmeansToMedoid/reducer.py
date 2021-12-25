
__authors__ = "Vaggelis Malandrakis, KLeio Fragkedaki + Applying to Probase addition by Jakub Perdek"

import json
import sys


def update_centroid_values(centroid_values: dict, concept_data) -> None:
    for typed_word_name, typed_word_value in concept_data.items():
        if typed_word_name in centroid_values:
            centroid_values[typed_word_name] = centroid_values[typed_word_name] + typed_word_value
        else:
            centroid_values[typed_word_name] = typed_word_value


def divide_values_by_count(centroid_values: dict, count: int = 1) -> None:
    for centroid_name, centroid_value in centroid_values.items():
        centroid_values[centroid_name] = (centroid_value + 0.0) / count


def calculate_new_centroids() -> None:
    current_centroid = None
    centroid_values = None
    centroid_index = -1
    count = 0

    # input comes from STDIN
    for line in sys.stdin:

        # parse the input of mapper.py
        centroid_index, concept_name, data = line.split('\t')
        concept_data = json.loads(data)

        # this IF-switch only works because Hadoop sorts map output
        # by key (here: word) before it is passed to the reducer
        if current_centroid == centroid_index:
            count += 1
            update_centroid_values(centroid_values, concept_data)
        else:
            if count != 0:
                # print the average of every cluster to get new centroids
                divide_values_by_count(centroid_values, count)
                print(current_centroid + "\t" + json.dumps(centroid_values))

            current_centroid = centroid_index
            centroid_values = concept_data
            count = 1

    # print last cluster's centroids
    if current_centroid == centroid_index and count != 0:
        divide_values_by_count(centroid_values, count)
        print(str(centroid_index) + "\t" + json.dumps(centroid_values))


if __name__ == "__main__":
    calculate_new_centroids()
