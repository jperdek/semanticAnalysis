import re
import math
import numpy as np
import json

separator = '\t'
clusters = dict()


def evaluate_cosine_weight(dict_vector1: dict, dict_vector2: dict) -> float:
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
    if bottom_value_vector1 * bottom_value_vector2 == 0:
        return 1.0
    return 1.0 - upper_value / (0.0 + bottom_value_vector1 * bottom_value_vector2)


def parse_input_vector(line_parts_v: [str], sample_instance: dict) -> None:
    for line_part in line_parts_v[1:len(line_parts_v) - 1]:
        result = re.search(r'^([^(]*)\(([^)]*)\)$', line_part)
        vector_name = result.group(1)
        vector_value = float(result.group(2))
        sample_instance[vector_name] = vector_value


def read_cluster(clusters_instance: dict, cluster_parts: list):
    created_cluster_name = cluster_parts[1]
    clusters_instance[created_cluster_name] = json.loads(cluster_parts[2])

    # some clusters shouldn't be connected, but if number of clusters must remain same following
    # print is necessary
    whole_cluster_instance = dict()
    whole_cluster_instance[created_cluster_name] = clusters_instance[created_cluster_name]
    print(created_cluster_name + ":" + json.dumps(whole_cluster_instance) + ";")


with open(0, "r", encoding="utf-8") as file:
    for line in file:
        min_distance = float('inf')
        line_parts = line.split(separator)
        if line_parts[0] == 'C':
            read_cluster(clusters, line_parts)
            continue
        elif line_parts[0] == 'S':
            sample = json.loads(line_parts[2])
        else:
            continue

        for cluster_name, cluster_vectors in clusters.items():
            distance = evaluate_cosine_weight(sample, cluster_vectors)
            if distance < min_distance:
                min_distance = distance
                whole_cluster = dict()
                whole_cluster[cluster_name] = clusters[cluster_name]
                chosen_cluster = whole_cluster
                printed_cluster_name = cluster_name

        whole_sample = dict()
        whole_sample[line_parts[1]] = sample
        print(printed_cluster_name + ":" + json.dumps(chosen_cluster) + ";" + json.dumps(whole_sample))
