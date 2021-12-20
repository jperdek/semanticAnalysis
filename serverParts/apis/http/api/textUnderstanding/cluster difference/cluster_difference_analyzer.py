
def read_cluster_file(file_name: str, process_dict: dict) -> None:
    process_dict[file_name] = dict()
    with open(file_name, "r") as file:
        for line in file:
            (sign, first_cluster, data, cluster_name, empty) = line.replace("\\n\"", "").replace("\n", "").split('\t')
            process_dict[file_name][cluster_name] = cluster_name


def sort_clusters_according_file(process_dict: dict) -> dict:
    sorted_file_clusters = dict()
    for file_name, file_clusters in process_dict.items():
        for cluster_name in file_clusters.keys():
            if cluster_name not in sorted_file_clusters:
                sorted_file_clusters[cluster_name] = list()
            sorted_file_clusters[cluster_name].append(file_name)
    return sorted_file_clusters


def find_not_included_clusters(file_clusters):
    for cluster_name, files in file_clusters.items():
        if len(files) == 1:
            print(cluster_name)


def process_all_files():
    process_dict = dict()
    read_cluster_file("clusters80.txt", process_dict)
    read_cluster_file("clusters81.txt", process_dict)
    read_cluster_file("clusters82.txt", process_dict)
    file_clusters = sort_clusters_according_file(process_dict)
    find_not_included_clusters(file_clusters)


if __name__ == '__main__':
    process_all_files()