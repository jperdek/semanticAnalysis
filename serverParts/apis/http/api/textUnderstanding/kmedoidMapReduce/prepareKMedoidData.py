try:
    from textUnderstanding.conceptDataNormalization.conceptVectorNormalization.conceptVectorNormalizationTools \
        import ConceptVectorNormalizationTools
except ImportError:
    from serverParts.apis.http.api.textUnderstanding.conceptDataNormalization.conceptVectorNormalizationTools \
        import ConceptVectorNormalizationTools
import random
import json


def load_values(file_name: str, result_dict: dict):
    number_lines = 0
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            number_lines = number_lines + 1

            text1, text2, value = line.split('\t')
            if len(text1.split()) > 1 or len(text2.split()) > 1:
                continue

            if text2 not in result_dict:
                result_dict[text2] = dict()
            if number_lines % 1000000 == 0:
                print(1000000)

            # uncomment for testing purposes - set number clusters to 100 for example
            # if len(result_dict) > 200000:
            #    result_dict[text2][text1] = float(value)
            #    break

            result_dict[text2][text1] = float(value)
    print("Whole length: " + str(len(result_dict)))


def save_values_for_kmedoid(result_dict: dict, file_name: str, separator='\t'):
    with open(file_name, "w", encoding="utf-8") as file:
        for context_key, context in result_dict.items():
            vector_position_values = ""
            for vector_position_name, vector_position_value in context.items():
                vector_position_values = vector_position_values + separator \
                                         + vector_position_name + "(" + \
                                         str(vector_position_value).replace('\n', '') + ")"
            add_length = separator + str(len(context.keys()))
            # separator between them should be included in second variable
            file.write(context_key + vector_position_values + add_length + "\n")


def write_record_to_file(file: any, context_key: str, context: dict, separator='\t'):
    vector_position_values = ""
    for vector_position_name, vector_position_value in context.items():
        vector_position_values = vector_position_values + separator \
                                 + vector_position_name + "(" + \
                                 str(vector_position_value) + ")"
    add_length = separator + str(len(context.keys()))
    # separator between them should be included in second variable
    file.write(context_key + vector_position_values + add_length + "\n")


def write_record_to_file_as_json(file: any, context_key: str, context: dict, separator='\t'):
    add_length = separator + str(len(context.keys()))
    file.write(context_key + separator + json.dumps(context) + add_length + "\n")


def write_record_to_file_as_json_typed(file: any, context_key: str, context: dict, type: str, separator='\t'):
    add_length = separator + str(len(context.keys()))
    file.write(type + separator + context_key + separator + json.dumps(context) + separator + context_key + add_length + "\n")


def save_values_for_kmedoid_and_clusters(result_dict: dict,
                                         cluster_indexes: list,
                                         record_file_name: str,
                                         cluster_file_name: str,
                                         separator='\t'):
    with open(cluster_file_name, "w", encoding="utf-8") as cluster_file:
        with open(record_file_name, "w", encoding="utf-8") as record_file:
            for index, (context_key, context) in enumerate(result_dict.items()):
                if index not in cluster_indexes:
                    write_record_to_file(record_file, context_key, context, separator)
                else:
                    write_record_to_file(cluster_file, context_key, context, separator)


def save_values_for_kmedoid_and_clusters_json(result_dict: dict,
                                              cluster_indexes: list,
                                              record_file_name: str,
                                              cluster_file_name: str,
                                              separator='\t'):
    with open(cluster_file_name, "w", encoding="utf-8") as cluster_file:
        with open(record_file_name, "w", encoding="utf-8") as record_file:
            for index, (context_key, context) in enumerate(result_dict.items()):
                if index not in cluster_indexes:
                    write_record_to_file_as_json(record_file, context_key, context, separator)
                else:
                    write_record_to_file_as_json(cluster_file, context_key, context, separator)


def save_values_for_kmedoid_and_clusters_json_typed(result_dict: dict,
                                                    cluster_indexes: list,
                                                    record_file_name: str,
                                                    separator='\t'):
    with open(record_file_name, "w", encoding="utf-8") as record_file:
        for index, (context_key, context) in enumerate(result_dict.items()):
            if index in cluster_indexes:
                write_record_to_file_as_json_typed(record_file, context_key, context, "C", separator)
        for index, (context_key, context) in enumerate(result_dict.items()):
            if index not in cluster_indexes:
                write_record_to_file_as_json_typed(record_file, context_key, context, "S", separator)

    with open('test/mrjob/dataonly1.txt', "w", encoding="utf-8") as record_file:
        for index, (context_key, context) in enumerate(result_dict.items()):
            if index not in cluster_indexes:
                write_record_to_file_as_json_typed(record_file, context_key, context, "S", separator)

    with open('test/mrjob/clusteronly1.txt', "w", encoding="utf-8") as record_file:
        for index, (context_key, context) in enumerate(result_dict.items()):
            if index in cluster_indexes:
                write_record_to_file_as_json_typed(record_file, context_key, context, "C", separator)


def create_random_array(length: int, max_iterations: int) -> list:
    array = list(range(0, length))
    for i in range(0, length):
        position = random.randrange(i, length)
        pom = array[position]
        array[position] = array[i]
        array[i] = pom
        if i > max_iterations:
            break
    return array[0:max_iterations]


if __name__ == "__main__":
    number_clusters = 2000
    # number_clusters = 100  # for testing
    generate_clusters = True
    save_normalization = False

    main_result_dict = dict()
    load_values('D://dipldatasets/data-concept-instance-relations.txt', main_result_dict)
    if not generate_clusters:
        save_values_for_kmedoid(main_result_dict, 'D://dipldatasets/data-concept-instance-relations-remake2.txt')
    else:
        chosen_clusters = create_random_array(len(main_result_dict.keys()), number_clusters)
        save_values_for_kmedoid_and_clusters(main_result_dict, chosen_clusters, 'test/algorithmDevelopment/data.txt',
                                             'test/algorithmDevelopment/clusters.txt')
        save_values_for_kmedoid_and_clusters_json(main_result_dict, chosen_clusters,
                                                  'test/data0.txt', 'test/clusters1.txt')
        save_values_for_kmedoid_and_clusters_json_typed(main_result_dict, chosen_clusters,
                                                        'test/algorithmDevelopment/typed/typdata.txt')

    if save_normalization:
        # normalize values
        ConceptVectorNormalizationTools.save_values_for_kmedoid_concept_normalized(
            main_result_dict, 'D://dipldatasets/data-concept-instance-relations-remake-normalized.txt')
        ConceptVectorNormalizationTools.save_values_for_kmedoid_concept_normalized_as_dict(
            main_result_dict, 'D://dipldatasets/data-concept-instance-relations-remake-normalized.json')
