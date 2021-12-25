import json


def apply_mapping_to_json(cluster_data: dict,
                          mapping_dictionary_from: dict,
                          mapping_dictionary_to: dict,
                          number: dict,
                          replacement="[{x}]"):
    for key, value in list(cluster_data.items()):
        if type(value) is dict or type(value) is list:
            apply_mapping_to_json(value,
                                  mapping_dictionary_from, mapping_dictionary_to,
                                  number, replacement)
        else:
            if key not in mapping_dictionary_to:
                mapping_dictionary_from[replacement.format(x=number["number"])] = key
                mapping_dictionary_to[key] = replacement.format(x=number["number"])
                number["number"] = number["number"] + 1
            new_key = mapping_dictionary_to[key]
            cluster_data[new_key] = cluster_data[key]
            del cluster_data[key]


def save_as_json(data: dict, file_name: str) -> None:
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(json.dumps(data))


def load_as_json(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def create_dict_clusters(input_cluster_file: str, output_cluster_file: str, dictionary_file: str,
                         mapping_dictionary_from=None, mapping_dictionary_to=None, number: dict = None) -> None:
    if mapping_dictionary_to is None:
        mapping_dictionary_to = dict()
    if mapping_dictionary_from is None:
        mapping_dictionary_from = dict()
    replacement = "[{x}]"
    if not number:
        number = dict()
        number["number"] = 0
    with open(output_cluster_file, "w", encoding="utf-8") as new_cluster_file:
        with open(input_cluster_file, "r", encoding="utf-8") as cluster_file:
            for line in cluster_file:
                cluster_name, initial_data, data = line.split('\t')
                cluster_data = json.loads(data)
                initial_cluster_data = json.loads(initial_data)
                if cluster_name not in mapping_dictionary_to:
                    mapping_dictionary_from[replacement.format(x=number["number"])] = cluster_name
                    mapping_dictionary_to[cluster_name] = replacement.format(x=number["number"])
                    number["number"] = number["number"] + 1
                new_cluster_name = mapping_dictionary_to[cluster_name]
                apply_mapping_to_json(cluster_data,
                                      mapping_dictionary_from, mapping_dictionary_to,
                                      number, replacement)
                apply_mapping_to_json(initial_cluster_data,
                                      mapping_dictionary_from, mapping_dictionary_to,
                                      number, replacement)
                new_cluster_file.write(new_cluster_name +
                                       "\t" + json.dumps(initial_cluster_data) +
                                       "\t" + json.dumps(cluster_data) + "\n")
        save_as_json(mapping_dictionary_from, dictionary_file)


def create_dict_data(input_cluster_file: str, output_cluster_file: str, dictionary_file: str,
                     mapping_dictionary_from=None, mapping_dictionary_to=None,
                     number: dict = None) -> None:
    if mapping_dictionary_to is None:
        mapping_dictionary_to = dict()
    if mapping_dictionary_from is None:
        mapping_dictionary_from = dict()
    replacement = "[{x}]"
    if not number:
        number = dict()
        number["number"] = 0
    with open(output_cluster_file, "w", encoding="utf-8") as new_cluster_file:
        with open(input_cluster_file, "r", encoding="utf-8") as cluster_file:
            for line in cluster_file:
                cluster_name, data = line.split('\t')
                cluster_data = json.loads(data)
                if cluster_name not in mapping_dictionary_to:
                    mapping_dictionary_from[replacement.format(x=number["number"])] = cluster_name
                    mapping_dictionary_to[cluster_name] = replacement.format(x=number["number"])
                    number["number"] = number["number"] + 1
                new_cluster_name = mapping_dictionary_to[cluster_name]
                apply_mapping_to_json(cluster_data,
                                      mapping_dictionary_from, mapping_dictionary_to,
                                      number, replacement)

                new_cluster_file.write(new_cluster_name + "\t" + json.dumps(cluster_data) + "\n")
        save_as_json(mapping_dictionary_from, dictionary_file)


def apply_de_mapping_to_json(cluster_data: dict, mapping_dictionary_from: dict):
    for key, value in list(cluster_data.items()):
        if type(value) is dict or type(value) is list:
            apply_de_mapping_to_json(value, mapping_dictionary_from)
        else:
            new_key = mapping_dictionary_from[key]
            cluster_data[new_key] = cluster_data[key]
            del cluster_data[key]


def de_mapping_clusters(optimized_clusters_file: str, new_file: str, mapping_from_dict_file: str) -> None:
    mapping_from_dict = load_as_json(mapping_from_dict_file)

    with open(new_file, "w", encoding="utf-8") as de_optimized_file:
        with open(optimized_clusters_file, "r", encoding="utf-8") as optimized_file:
            for line in optimized_file:
                cluster_name, initial_data, data = line.split('\t')
                cluster_data = json.loads(data)
                initial_cluster_data = json.loads(initial_data)
                old_cluster_name = mapping_from_dict[cluster_name]
                apply_de_mapping_to_json(cluster_data, mapping_from_dict)
                apply_de_mapping_to_json(initial_cluster_data, mapping_from_dict)
                de_optimized_file.write(old_cluster_name + "\t" +
                                        json.dumps(initial_cluster_data) + "\t" +
                                        json.dumps(cluster_data) + "\n")


def de_mapping_data(optimized_clusters_file: str, new_file: str, mapping_from_dict_file: str) -> None:
    mapping_from_dict = load_as_json(mapping_from_dict_file)

    with open(new_file, "w", encoding="utf-8") as de_optimized_file:
        with open(optimized_clusters_file, "r", encoding="utf-8") as optimized_file:
            for line in optimized_file:
                cluster_name, data = line.split('\t')
                cluster_data = json.loads(data)

                old_cluster_name = mapping_from_dict[cluster_name]
                apply_de_mapping_to_json(cluster_data, mapping_from_dict)
                de_optimized_file.write(old_cluster_name + "\t" + json.dumps(cluster_data) + "\n")


if __name__ == "__main__":
    mapping_to = dict()
    mapping_from = dict()
    number_map = dict()
    number_map["number"] = 0

    # OPTIMIZING CLUSTERS
    create_dict_clusters("../clusters0.txt", "optimized_clusters.txt", "example_mapping_dict.json",
                         mapping_from, mapping_to, number_map)

    # RETURNING BACK
    de_mapping_clusters("optimized_clusters.txt", "de-optimized_clusters.txt", "example_mapping_dict.json")

    # OPTIMIZING
    create_dict_data("../data0.txt", "optimized_data.txt", "example_mapping_dict_updated.json",
                     mapping_from, mapping_to, number_map)

    # RETURNING BACK
    de_mapping_data("optimized_data.txt", "de-optimized_data.txt", "example_mapping_dict_updated.json")
