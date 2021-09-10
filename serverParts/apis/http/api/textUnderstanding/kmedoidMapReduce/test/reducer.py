import json
import math

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

for index, cluster in enumerate(clusters):
    cluster_name = list(cluster.keys())[0]
    if numbers[index] == 0:
        print(cluster_name + ":" + json.dumps(cluster) + ";" + json.dumps(cluster[cluster_name]))
    # else:
    #    print(cluster)