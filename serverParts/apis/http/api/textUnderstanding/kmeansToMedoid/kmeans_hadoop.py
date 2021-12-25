import os


def file_data_are_same(cluster_file1: str, cluster_file2: str) -> bool:
    comparison_dict1: dict = dict()
    comparison_dict2: dict = dict()
    with open(cluster_file1, "r", encoding="utf-8") as cluster_file1:
        for line in cluster_file1:
            parsed_cluster_file1 = line.split('\t')
            comparison_dict1[parsed_cluster_file1[0]] = parsed_cluster_file1[2]

    with open(cluster_file2, "r", encoding="utf-8") as cluster_file2:
        for line in cluster_file2:
            parsed_cluster_file2 = line.split('\t')
            comparison_dict2[parsed_cluster_file2[0]] = parsed_cluster_file2[2]

    return comparison_dict1 == comparison_dict2


def launch(data_path="/k-means/data0.txt", iteration: int = 1):
    print("Removing output: /k-means/output*")
    os.system("hadoop fs -rm -R /k-means/output*")

    print("Uploading files: data0.txt")
    os.system("hadoop fs -mkdir /k-means")
    os.system("hadoop fs -copyFromLocal -f ./data0.txt /k-means/data0.txt")

    while True:
        print("Executing iteration: " + str(iteration))
        os.system("hadoop jar ./hadoop-streaming-3.2.1.jar "
                  "-file clusters" + str(iteration - 1) + ".txt "
                  "-file ./mapper.py -mapper \"python3 ./mapper.py clusters" + str(iteration - 1) + ".txt\" "
                  "-file ./reducer.py -reducer \"python3 ./reducer.py\" "
                  "-input " + data_path + " "
                  "-output /k-means/output" + str(iteration))

        print("Performing copying and cleaning: ")
        os.system("hadoop fs -copyToLocal -f /k-means/output" +
                  str(iteration) + "/part-00000 ./cluster-temp.txt")
        os.system("hadoop fs -rm -R /k-means/output" + str(iteration))

        print("Performing to medoid update: ")
        os.system("python3 cluster_updater.py < ./cluster-temp.txt > ./clusters" + str(iteration) + ".txt")

        print("Comparing cluster files clusters" + str(iteration - 1) + ".txt and clusters" + str(iteration) + ".txt:")
        if file_data_are_same("clusters" + str(iteration - 1) + ".txt", "clusters" + str(iteration) + ".txt"):
            break
        iteration = iteration + 1


if __name__ == "__main__":
    launch()
