import os


def file_data_are_same(cluster_file1: str, cluster_file2: str) -> bool:
    comparison_dict1: dict = dict()
    comparison_dict2: dict = dict()
    with open(cluster_file1, "r", encoding="utf-8") as cluster_file1:
        for line in cluster_file1:
            parsed_cluster_file1 = line.split('\t')
            comparison_dict1[parsed_cluster_file1[0]] = parsed_cluster_file1[1]

    with open(cluster_file2, "r", encoding="utf-8") as cluster_file2:
        for line in cluster_file2:
            parsed_cluster_file2 = line.split('\t')
            comparison_dict2[parsed_cluster_file2[0]] = parsed_cluster_file2[1]

    return comparison_dict1 == comparison_dict2


def launch(data_path="/k-means/data0.txt", iteration: int = 1):
    print("Removing output: /k-means/output*")
    os.system("hadoop fs -rm -R /k-means/output*")

    print("Uploading files: clusters0.txt and data0.txt")
    os.system("hadoop fs -mkdir /k-means")
    os.system("hadoop fs -copyFromLocal ./data0.txt /k-means/data0.txt")
    os.system("hadoop fs -copyFromLocal ./clusters0.txt /k-means/clusters0.txt")
    os.system("hadoop fs -copyFromLocal ./clusters0.txt ./clusters0.txt")
    while True:
        print("Executing iteration: " + str(iteration))
        os.system("hadoop jar ./hadoop-streaming-3.2.1.jar "
                  "-file clusters0.txt "
                  "-file ./mapper.py -mapper \"python3 ./mapper.py\" "
                  "-file ./reducer.py -reducer \"python3 ./reducer.py\" "
                  "-input " + data_path + " "
                                          "-output /k-means/output" + str(iteration))
        os.system(
            "hadoop fs -copyToLocal /k-means/output" +
            str(iteration) + "/part-00000 ./clusters" + str(iteration) + ".txt")
        iteration = iteration + 1
        if file_data_are_same("clusters" + str(iteration - 1) + ".txt", "clusters" + str(iteration) + ".txt"):
            break


if __name__ == "__main__":
    launch()
