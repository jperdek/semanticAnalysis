try:
    from textUnderstanding.kmeansToMedoid.clean_data import clean_output_data
    from textUnderstanding.kmeansToMedoid.optimization.dictionary_manager import \
        create_dict_clusters, create_dict_data, de_mapping_clusters, de_mapping_data
    from textUnderstanding.kmedoidMapReduce.prepareKMedoidData import load_values, \
        save_values_for_kmedoid_and_clusters_json, create_random_array
except ImportError:
    try:
        from apis.http.api.textUnderstanding.kmeansToMedoid.clean_data import clean_output_data
        from apis.http.api.textUnderstanding.kmeansToMedoid.optimization.dictionary_manager import \
            create_dict_clusters, create_dict_data, de_mapping_clusters, de_mapping_data
        from apis.http.api.textUnderstanding.kmedoidMapReduce.prepareKMedoidData import load_values, \
            save_values_for_kmedoid_and_clusters_json, create_random_array
    except ImportError:
        from serverParts.apis.http.api.textUnderstanding.kmeansToMedoid.clean_data import clean_output_data
        from serverParts.apis.http.api.textUnderstanding.kmeansToMedoid.optimization.dictionary_manager import \
            create_dict_clusters, create_dict_data, de_mapping_clusters, de_mapping_data
        from serverParts.apis.http.api.textUnderstanding.kmedoidMapReduce.prepareKMedoidData import load_values, \
            save_values_for_kmedoid_and_clusters_json, create_random_array


def optimize():
    mapping_to = dict()
    mapping_from = dict()
    number_map = dict()
    number_map["number"] = 0

    # OPTIMIZING
    create_dict_data("./use/datad.txt", "./use/data0.txt", "./use/mapping_dict.json",
                     mapping_from, mapping_to, number_map)

    # RETURNING BACK
    de_mapping_data("./use/data0.txt", "./use/de-data0.txt", "./use/mapping_dict.json")

    # OPTIMIZING CLUSTERS
    create_dict_clusters("./use/clustersd.txt", "./use/clusters0.txt", "./use/mapping_dict.json",
                         mapping_from, mapping_to, number_map)

    # RETURNING BACK
    de_mapping_clusters("./use/clusters0.txt", "./use/de-clusters0.txt", "./use/mapping_dict.json")


if __name__ == "__main__":
    number_clusters = 2000
    # number_clusters = 100  # for testing
    generate_clusters = True
    save_normalization = False

    main_result_dict = dict()
    load_values('D://dipldatasets/data-concept-instance-relations.txt', main_result_dict)
    chosen_clusters = create_random_array(len(main_result_dict.keys()), number_clusters)
    save_values_for_kmedoid_and_clusters_json(main_result_dict, chosen_clusters,
                                              '../kmedoidMapReduce/test/datad.txt',
                                              '../kmedoidMapReduce/test/clustersd.txt')
    clean_output_data("../kmedoidMapReduce/test/datad.txt", "./use/datad.txt", False)
    clean_output_data("../kmedoidMapReduce/test/clustersd.txt", "./use/clustersd.txt", True)
    optimize()
