import json
import numpy as np
import math


map_separator = ';'
actual_cluster_name = None
cluster_samples = dict()


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


def evaluate_mid_sample_value(cluster_samples_instance: dict, chosen_sample_data: dict):
    whole_distance = 0.0
    for other_sample_data in cluster_samples_instance.values():
        whole_distance = whole_distance + evaluate_cosine_weight(chosen_sample_data, other_sample_data)
    return whole_distance


def find_sample_minimum(cluster_data_instance: dict):
    min_distance = float('inf')
    minimal_sample = None

    for repeat_sample_name, repeat_sample_data in cluster_data_instance.items():
        distance = evaluate_mid_sample_value(cluster_data_instance, repeat_sample_data)
        #print(distance)
        if distance < min_distance:
            min_distance = distance
            whole_repeat_sample = dict()
            whole_repeat_sample[repeat_sample_name] = repeat_sample_data
            minimal_sample = whole_repeat_sample

    return minimal_sample


with open(0, "r", encoding="utf-8") as file:
    for line in file:
        cluster_info_data, sample_text_data = line.split(map_separator)
        cluster_name, cluster_text_data = cluster_info_data.split(':', 1)
        cluster = json.loads(cluster_text_data)

        if sample_text_data != "\n" and sample_text_data != "":
            sample = json.loads(sample_text_data)
            sample_name = list(sample.keys())[0]
            sample_data = list(sample.values())[0]
            cluster_data = list(sample.values())[0]

        if actual_cluster_name is not None and cluster_name != actual_cluster_name:
            minimal_sample_result = find_sample_minimum(cluster_samples)
            print(json.dumps(previous_cluster) + ";" + json.dumps(minimal_sample_result)
                  + ';' + str(len(cluster_samples.keys())))

            # new cluster init
            cluster_samples = dict()                # null dict for new cluster

        actual_cluster_name = cluster_name       # set new name
        previous_cluster = cluster
        if sample_text_data != "\n" and sample_text_data != "":
            cluster_samples[sample_name] = sample_data

# for last line
minimal_sample_result = find_sample_minimum(cluster_samples)
print(json.dumps(previous_cluster) + ";" + json.dumps(minimal_sample_result) + ';' + str(len(cluster_samples.keys())))
