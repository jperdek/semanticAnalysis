import sys


def update_clusters_ordered_by_numbers(old_cluster_filename: str) -> None:
    cluster_index = 0
    with open(old_cluster_filename, "r", encoding="utf-8") as old_clusters_file:
        clusters_line = next(old_clusters_file)
        cluster_name, initial_data, means_data = clusters_line.split("\t")

        for input_line in sys.stdin:
            input_line = input_line.strip()
            input_cluster_index, modified_means_data = input_line.split("\t")
            input_cluster_index = int(input_cluster_index)

            # INDEX FOR CLUSTER NOT MATCH - TRYING TO GET TO DATA CLUSTER INDEX
            if input_cluster_index > cluster_index:
                print(cluster_name + "\t" + initial_data + "\t" + means_data + "\t")

                while input_cluster_index > cluster_index:
                    clusters_line = next(old_clusters_file)
                    cluster_name, initial_data, means_data = clusters_line.split("\t")
                    cluster_index = cluster_index + 1

                    if input_cluster_index > cluster_index:
                        print(cluster_name + "\t" + initial_data + "\t" + means_data + "\t")
            print(str(input_cluster_index) + " " + str(cluster_index))

            # DATA IN CLUSTER ARE MODIFIED - in the end new cluster can be loaded
            if input_cluster_index == cluster_index:
                print(cluster_name + "\t" + initial_data + "\t" + modified_means_data + "\n")

                clusters_line = next(old_clusters_file)
                cluster_name, initial_data, means_data = clusters_line.split("\t")
                cluster_index = cluster_index + 1
                continue

            # CLUSTER INDEX SHOULD NOT BE LOWER
            if input_cluster_index < cluster_index:
                print(str(input_cluster_index) + " " + str(cluster_index))
                raise Exception("Cluster index should not be lower")


if __name__ == "__main__":
    update_clusters_ordered_by_numbers("../clusters0.txt")
