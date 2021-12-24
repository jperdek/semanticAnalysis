import sys


def update_clusters(old_cluster_filename: str) -> None:
    clusters = dict()
    with sys.stdin as input_file:
        for new_clusters_line in input_file:
            new_clusters_line = new_clusters_line.strip()
            input_cluster_index, modified_means_data = new_clusters_line.replace("\n", "").split("\t")
            clusters[str(input_cluster_index)] = modified_means_data

    with open(old_cluster_filename, "r", encoding="utf-8") as old_clusters_file:
        for old_cluster_index, old_cluster_line in enumerate(old_clusters_file):
            cluster_name, initial_data, means_data = old_cluster_line.replace("\n", "").split("\t")
            if str(old_cluster_index) in clusters:
                modified_means_data = clusters[str(old_cluster_index)]
                print(cluster_name + "\t" + initial_data + "\t" + modified_means_data)
            else:
                print(cluster_name + "\t" + initial_data + "\t" + means_data)

if __name__ == "__main__":
    update_clusters("clusters0.txt")
