import json

from serverParts.apis.http.api.textUnderstanding.kMedoidConceptData.kMedoid import associate_medoids_to_closest_one, \
    save_results


def analyze(data_associations: dict) -> dict:
    statistics = dict()
    for cluster_name, data_names in data_associations.items():
        print(cluster_name + " " + str(len(data_names)))
        count = str(len(data_names))
        if count not in statistics:
            statistics[count] = 0
        statistics[count] = statistics[count] + 1

    for word, value in statistics.items():
        print(word +" " + str(value))
    return statistics


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_clusters(clusters_file_name: str) -> dict:
    clusters_dict = dict()
    line_number = 0
    with open(clusters_file_name, "r") as file:
        for line in file:
            (sign, first_cluster, data, cluster_name, empty) = \
                line.replace("\\n\"", "").replace("\n", "").replace("\\n", "").split(
                    '\t')
            line_number = line_number + 1
            if line_number > 200:
                break
            elif line_number > 100:
                clusters_dict[cluster_name] = json.loads(data)
    return clusters_dict


def load_data(data_file_name: str) -> dict:
    data_dict = dict()
    with open(data_file_name, "r") as file:
        for line in file:
            (sign, data_name, data, data_name2) = line.split('\t')
            data_dict[data_name2] = json.loads(data)
    return data_dict


def k_medoid_algorithm(file_name: str = "groups1.json") -> None:
    distance = dict()
    clusters = load_clusters("C:\\Users\\perde\\clusters57.txt")
    random_k_medoids_keys = list(clusters.keys())
    result_dict = load_data("C:\\Users\\perde\\data57.txt")
    print("Initial asociation of medoids started:")
    result_dict.update(clusters)
    result_connections = associate_medoids_to_closest_one(random_k_medoids_keys, result_dict, distance)

    print("Saving results")
    save_results(result_connections, file_name)


if __name__ == '__main__':
    # k_medoid_algorithm()
    associations = load_as_json("groups1.json")
    print(analyze(associations))
