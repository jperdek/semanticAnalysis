import json
import math
import numpy as np
import sys

separator = ";"
samples = list()
numbers = list()
clusters = list()


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


with open(0, "r", encoding="utf-8") as file:
    for line in file:
        cluster, mid_value, number = line.split(separator)
        clusters.append(json.loads(cluster))
        samples.append(json.loads(mid_value))
        numbers.append(int(number))

categorization_dict = dict()
for i, sample_dict in enumerate(samples):
    min_distance = float('inf')
    if sample_dict is not None:
        sample = list(sample_dict.values())[0]
        for cluster_dict in clusters:
            cluster = list(cluster_dict.values())[0]
            distance = evaluate_cosine_weight(cluster, sample)
            if distance < min_distance:
                min_distance = distance
                categorization_dict[i] = cluster

for index, cluster_dict in enumerate(clusters):
    cluster_name = list(cluster_dict.keys())[0]
    cluster = list(cluster_dict.values())[0]
    min_cluster = None
    min_sample_index = sys.maxsize
    for i, chosen_cluster in categorization_dict.items():
        i = int(i)
        if cluster == chosen_cluster:
            if min_sample_index == sys.maxsize:
                min_sample_index = i
            if numbers[i] >= numbers[min_sample_index]:
                min_sample_index = i
                min_cluster = chosen_cluster
    if min_cluster is not None:
        print(list(samples[min_sample_index].keys())[0])
        print("C\t" + list(samples[min_sample_index].keys())[0] + "\t" + json.dumps(list(samples[min_sample_index].values())[0])
              + "\t" + json.dumps(clusters[index]))
    else:
        print("C\t" + cluster_name + "\t" + json.dumps(cluster) + "\t" + json.dumps(clusters[index]))