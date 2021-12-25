import json
from math import sqrt


def analyze(data_associations: dict) -> dict:
    statistics = dict()
    for cluster_name, data_names in data_associations.items():
        print(cluster_name + " " + str(len(data_names)))
        count = str(len(data_names))
        if count not in statistics:
            statistics[count] = 0
        statistics[count] = statistics[count] + 1

    for word, value in statistics.items():
        print(word + " " + str(value))
    return statistics


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_clusters(clusters_file_name: str) -> dict:
    clusters_dict = dict()
    line_number = 0
    with open(clusters_file_name, "r") as file:
        for line in file:
            (cluster_name, initial_data, cluster_data) = line.split('\t')
            clusters_dict[cluster_name] = json.loads(cluster_data)
            line_number = line_number + 1
    return clusters_dict


def load_data(data_file_name: str) -> dict:
    data_dict = dict()
    with open(data_file_name, "r") as file:
        for line in file:
            (data_name, data) = line.split('\t')
            data_dict[data_name] = json.loads(data)
    return data_dict


def save_as_json(data: dict, file_name: str):
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(json.dumps(data))


def save_results(result_connections: dict, file_name) -> None:
    medoids = dict()
    for result_connection_key in result_connections.keys():
        if result_connections[result_connection_key]['medoid'] not in medoids:
            medoids[result_connections[result_connection_key]['medoid']] = list()
        medoids[result_connections[result_connection_key]['medoid']].append(result_connection_key)
    save_as_json(medoids, file_name)


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


def associate_medoids_to_closest_one(random_k_sample_keys: list, result_dict: dict, distance: dict, omit = False) -> dict:
    result_connections = dict()
    number_done = 0
    distance['previous'] = 0.0
    all_medoids = dict()

    for chosen_medoid_key in random_k_sample_keys:
        result_connections[chosen_medoid_key] = dict()
        result_connections[chosen_medoid_key]['medoid'] = chosen_medoid_key

    for point_to_associate_key in result_dict.keys():
        # point is not chosen to be medoid
        minimal_distance = None
        closest_medoid_key = None
        if point_to_associate_key not in random_k_sample_keys:
            for chosen_medoid_key in random_k_sample_keys:
                calculated_value = evaluate_cosine_weight(
                    result_dict[point_to_associate_key], result_dict[chosen_medoid_key])
                distance['previous'] = distance['previous'] + calculated_value

                if minimal_distance is None or minimal_distance > calculated_value:
                    minimal_distance = calculated_value
                    closest_medoid_key = chosen_medoid_key

            if not omit or minimal_distance < 1.0:
                result_connections[point_to_associate_key] = dict()
                result_connections[point_to_associate_key]['medoid'] = closest_medoid_key
                result_connections[point_to_associate_key]['dist'] = minimal_distance
                all_medoids[closest_medoid_key] = closest_medoid_key
        else:
            result_connections[point_to_associate_key] = dict()
            result_connections[point_to_associate_key]['medoid'] = point_to_associate_key
            result_connections[point_to_associate_key]['dist'] = 0

        if not omit and result_connections[point_to_associate_key]['medoid'] is None:
            print("Error: medoid cant be None: " + point_to_associate_key)

        number_done = number_done + 1
        if number_done % 100000 == 0:
            print("Done is: " + str(number_done / len(result_dict.keys())))
    return result_connections


def k_medoid_algorithm(file_name: str = "groups1.json") -> None:
    distance = dict()
    clusters = load_clusters("clusters14.txt")
    random_k_medoids_keys = list(clusters.keys())
    result_dict = load_data("data0.txt")
    print("Initial asociation of medoids started:")
    result_dict.update(clusters)
    result_connections = associate_medoids_to_closest_one(random_k_medoids_keys, result_dict, distance)

    print("Saving results")
    save_results(result_connections, file_name)


if __name__ == '__main__':
    k_medoid_algorithm()
    associations = load_as_json("groups1.json")
    print(analyze(associations))