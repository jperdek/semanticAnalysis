#!/usr/bin/env python
"""mapper.py"""

__authors__ = "Vaggelis Malandrakis, KLeio Fragkedaki + Applying to Probase addition by Jakub Perdek"

import sys
import json
from math import sqrt


def evaluate_cosine_weight(dict_vector1: dict, dict_vector2: dict) -> float:
    unique_keys = list(set(list(dict_vector1.keys()) + list(dict_vector2.keys())))
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

    bottom_value_vector1 = sqrt(bottom_value_vector1)
    bottom_value_vector2 = sqrt(bottom_value_vector2)
    if bottom_value_vector1 * bottom_value_vector2 == 0:
        return 1.0
    return 1.0 - upper_value / (0.0 + bottom_value_vector1 * bottom_value_vector2)


# get initial centroids from a txt file and add them in an array
def get_cluster_centroids(filepath: str) -> list:
    clusters = []

    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line:
                try:
                    line = line.strip()
                    cluster = dict()
                    cluster_name, initial_data, data = line.split('\t')
                    cluster_data = json.loads(data)
                    cluster[cluster_name] = cluster_data

                    clusters.append(cluster)
                except Exception as e:
                    print("Exceptions occurred: " + str(e))
                    break
            else:
                break
            line = fp.readline()

    fp.close()
    return clusters


# create clusters based on initial centroids
def create_clusters(clusters: list) -> None:
    # 
    for line in sys.stdin:
        line = line.strip()
        concept = dict()
        concept_name, data = line.split('\t')
        concept_data = json.loads(data)
        concept[concept_name] = concept_data

        min_dist = 100000000000000
        index = -1

        for cluster in clusters:
            cluster_name = list(cluster.keys())[0]
            # count distance
            # to every centroid
            cur_dist = evaluate_cosine_weight(cluster[cluster_name], concept[concept_name])

            # find the centroid which is closer to the point
            if cur_dist <= min_dist:
                min_dist = cur_dist
                index = clusters.index(cluster)

        print(str(index) + "\t" + concept_name + "\t" + data)


if __name__ == "__main__":
    clusters_data = get_cluster_centroids('clusters0.txt')
    create_clusters(clusters_data)
