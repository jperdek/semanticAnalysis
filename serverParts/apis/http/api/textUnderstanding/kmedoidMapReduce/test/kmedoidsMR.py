import os

def file_data_are_same(cluster_file1: str, cluster_file2: str) -> None:
    comparison_dict1: dict = dict()
    comparison_dict2: dict = dict()
    with open(cluster_file1, "r", encoding="utf-8") as cluster_file1:
        for line in cluster_file1:
            parsed_cluster_file1 = line.split('\t')
            comparison_dict1[parsed_cluster_file1[3]] = parsed_cluster_file1[2]

    with open(cluster_file2, "r", encoding="utf-8") as cluster_file2:
        for line in cluster_file2:
            parsed_cluster_file2 = line.split('\t')
            comparison_dict2[parsed_cluster_file2[3]] = parsed_cluster_file2[2]

    return comparison_dict1 == comparison_dict2
    
def divide_result_file(result_file: str,
                       iteration: int,
                       cluster_file_name='clusters1.txt',
                       data_file_name='data1.txt') -> None:
    with open(result_file, "r", encoding="utf-8") as all_file:
        with open(cluster_file_name, "w", encoding="utf-8") as cluster_file:
            with open(data_file_name, "w", encoding="utf-8") as data_file:
                for line in all_file:
                    if line[1] == 'C':
                        cluster_file.write(line[1:line.rfind('"\\n"') - 2].replace("\\t", "\t").replace('\\"', '"') + "\n")
                    elif line[1] == 'S':
                        data_file.write(line[1:line.rfind('"\\n"') - 2].replace("\\t", "\t").replace('\\"', '"') + "\n")
                    else:
                        print(line[1])
                        # print("Error: unknown line: " + line)
    
def test_of_similarity():
    print(file_data_are_same('clusteronly.txt', 'clusteronly1.txt'))
    print(file_data_are_same('clusteronly.txt', 'clusters1.txt'))
    
if __name__ == '__main__':
    iteration = 1

    while True:
        print("Executing iteration: " + str(iteration))
        os.system("python3 mrjobsync-hadoop.py data" + str(iteration - 1) + ".txt -r hadoop "
                  "--iteration " + str(iteration) + " --jobconf mapreduce.job.reducers=" + str(iteration) + 
                  " --clusters clusters" + str(iteration - 1) + ".txt --datafile data" + str(iteration - 1) + ".txt > data_clusters" + str(iteration) + ".txt")
        divide_result_file('data_clusters' + str(iteration) + '.txt', iteration, 'clusters' + str(iteration) + '.txt', 'data' + str(iteration) + '.txt')
        if file_data_are_same('clusters' + str(iteration - 1) + '.txt', 'clusters' + str(iteration) + '.txt'):
            print("Clusters not changed - finishing...")
            break
        iteration = iteration + 1
