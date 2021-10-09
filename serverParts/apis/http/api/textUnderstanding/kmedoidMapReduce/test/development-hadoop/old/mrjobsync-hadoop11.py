
from mrjob.job import MRJob
from mrjob.step import MRStep
import math
#import numpy as np
import json
import sys
import os
save_path = "."

class KMedoid(MRJob):
    MRJob.SORT_VALUES = True

    def configure_args(self):
        super(KMedoid, self).configure_args()
        self.add_passthru_arg("-i", "--iteration", help="Actual iteration")

    # MAPPER VARIABLES
    separator = '\t'

    # COMBINER VARIABLES

    # REDUCER VARIABLES
    cluster_connections = dict()
    real_cluster_names = dict()
    cluster_to_sample_connections = dict()
    samples = dict()
    numbers = dict()

    # MAPPER PART
    @staticmethod
    def evaluate_cosine_weight(dict_vector1: dict, dict_vector2: dict) -> float:
        unique_keys = list(set(list(dict_vector1.keys()) + list(dict_vector2.keys())))
        upper_value = 0.0
        bottom_value_vector1 = 0.0
        bottom_value_vector2 = 0.0
        for key in unique_keys:
            if key in dict_vector1 and key in dict_vector2:  # in other cases result will be zero
                upper_value = upper_value + float(dict_vector1[key]) * float(dict_vector2[key])
            if key in dict_vector1:  # in other cases added value will be zero
                bottom_value_vector1 = bottom_value_vector1 + pow(float(dict_vector1[key]), 2.0)
            if key in dict_vector2:  # in other cases added value will be zero
                bottom_value_vector2 = bottom_value_vector2 + pow(float(dict_vector2[key]), 2.0)

        bottom_value_vector1 = math.sqrt(bottom_value_vector1)
        bottom_value_vector2 = math.sqrt(bottom_value_vector2)
        if bottom_value_vector1 * bottom_value_vector2 == 0:
            return 1.0
        return 1.0 - upper_value / (0.0 + bottom_value_vector1 * bottom_value_vector2)

    @staticmethod
    def read_cluster(clusters_instance: dict, cluster_parts: list):
        created_cluster_name = cluster_parts[1]
        clusters_instance[created_cluster_name] = json.loads(cluster_parts[2])

        # some clusters shouldn't be connected, but if number of clusters must remain same following
        # print is necessary
        whole_cluster_instance = dict()
        whole_cluster_instance[created_cluster_name] = clusters_instance[created_cluster_name]
        yield created_cluster_name + ":" + json.dumps(whole_cluster_instance),

    def get_cluster_file_path(self):
        if self.options.iteration == '1':
            return save_path + 'clusteronly.txt'
        else:
            return save_path + '/' + str(int(self.options.iteration) - 1) + '/clusters' + str(int(self.options.iteration) - 1) + '.txt'

    def mapper_init(self):
        cluster_path = self.get_cluster_file_path()
        self.clusters = dict()
        self.names = dict()
        with open(cluster_path, "r", encoding="utf-8") as cluster_file:
            for cluster_line in cluster_file:
                # KMedoid.read_cluster(clusters_instance, cluster_line.split(self.separator))
                cluster_parts = cluster_line.split(self.separator)
                created_cluster_name = cluster_parts[1]
                self.clusters[created_cluster_name] = json.loads(cluster_parts[2])
                self.names[created_cluster_name] = cluster_parts[3]
                # some clusters shouldn't be connected, but if number of clusters must remain same following
                # print is necessary
                whole_cluster_instance = dict()
                whole_cluster_instance[created_cluster_name] = self.clusters[created_cluster_name]
                yield created_cluster_name + ":" + self.names[created_cluster_name] + ":" + json.dumps(whole_cluster_instance), ""
        print('INIT END')

    def mapper(self, _, line):
        line_parts = line.split(self.separator)
        if line_parts[0] == 'C':
            return
        elif line_parts[0] == 'S':
            sample = json.loads(line_parts[2])
        else:
            return
        min_distance = float('inf')
        printed_cluster_name = None
        chosen_cluster = None
        chosen_name = None
        for cluster_name, cluster_vectors in self.clusters.items():
            distance = self.evaluate_cosine_weight(sample, cluster_vectors)
            if distance < min_distance:
                min_distance = distance
                whole_cluster = dict()
                whole_cluster[cluster_name] = self.clusters[cluster_name]
                chosen_name = self.names[cluster_name]
                chosen_cluster = whole_cluster
                printed_cluster_name = cluster_name

        whole_sample = dict()
        whole_sample[line_parts[1]] = sample
        yield printed_cluster_name + ":" + chosen_name + ":" + json.dumps(chosen_cluster), json.dumps(whole_sample)

    # COMBINER PART

    @staticmethod
    def evaluate_mid_sample_value(cluster_samples_instance: dict, chosen_sample_data: dict):
        whole_distance = 0.0
        for other_sample_data in cluster_samples_instance.values():
            whole_distance = whole_distance + KMedoid.evaluate_cosine_weight(chosen_sample_data, other_sample_data)
        return whole_distance

    @staticmethod
    def find_sample_minimum(cluster_data_instance: dict):
        min_distance = float('inf')
        minimal_sample = None

        for repeat_sample_name, repeat_sample_data in cluster_data_instance.items():
            distance = KMedoid.evaluate_mid_sample_value(cluster_data_instance, repeat_sample_data)
            # print(distance)
            if distance < min_distance:
                min_distance = distance
                whole_repeat_sample = dict()
                whole_repeat_sample[repeat_sample_name] = repeat_sample_data
                minimal_sample = whole_repeat_sample

        return minimal_sample

    # works only after specific local map!!! - same needs to be done on reducer
    def combiner(self, cluster_info_data, sample_text_data_list):
        # new cluster init
        print('COMBINER')
        cluster_samples = dict()  # null dict for new cluster
        cluster_name, real_cluster_name, cluster_text_data = cluster_info_data.split(':', 2)
        cluster = json.loads(cluster_text_data)
        for sample_text_data in list(sample_text_data_list):
            if sample_text_data != "\n" and sample_text_data != "":
                sample = json.loads(sample_text_data)
                sample_name = list(sample.keys())[0]
                sample_data = list(sample.values())[0]
                cluster_samples[sample_name] = sample_data
            else:
                continue
        minimal_sample_result = self.find_sample_minimum(cluster_samples)
        yield real_cluster_name + ";" + json.dumps(cluster), str(json.dumps(minimal_sample_result) + ';' + str(len(cluster_samples.keys())))

    # REDUCER PART
    @staticmethod
    def get_data_file_path(iteration: int):
        return save_path + '/data' + str(iteration) + '.txt'

    @staticmethod
    def get_base_path():
        return save_path + '/dataonly.txt'

    @staticmethod
    def evaluate_mid_sample_value_from_list(cluster_samples_instance: list, chosen_sample_data: dict):
        whole_distance = 0.0
        for other_sample_data_str in cluster_samples_instance:
            extracted_cluster_data_str = other_sample_data_str.split(';')[0]
            if extracted_cluster_data_str != "null":
                other_data_instance = json.loads(extracted_cluster_data_str)
                other_sample_data = list(other_data_instance.values())[0]
                whole_distance = whole_distance + KMedoid.evaluate_cosine_weight(chosen_sample_data, other_sample_data)
        return whole_distance

    @staticmethod
    def find_sample_minimum_from_list(cluster_data_list: list):
        min_distance = float('inf')
        minimal_sample = None
        associated_value = 0
        for cluster_data_instance_str in cluster_data_list:
            line_content = cluster_data_instance_str.split(';')
            extracted_cluster_data_str = line_content[0]
            if extracted_cluster_data_str != "null":
                cluster_data_instance = json.loads(extracted_cluster_data_str)
                repeat_sample_name = list(cluster_data_instance.keys())[0]
                repeat_sample_data = list(cluster_data_instance.values())[0]
                distance = KMedoid.evaluate_mid_sample_value_from_list(cluster_data_list, repeat_sample_data)
                # print(distance)
                if distance < min_distance:
                    min_distance = distance
                    whole_repeat_sample = dict()
                    whole_repeat_sample[repeat_sample_name] = repeat_sample_data
                    minimal_sample = whole_repeat_sample

                associated_value = associated_value + int(line_content[1])
        return minimal_sample, associated_value

    def reducer(self, cluster_and_name, min_cluster_candidates):
        real_cluster_name, cluster = cluster_and_name.split(';', 1)
        minimal_sample_result_mid_value, number = self.find_sample_minimum_from_list(list(min_cluster_candidates))
        cluster_instance = json.loads(cluster)
        cluster_name = list(cluster_instance.keys())[0]

        if number != 0:  # and str(minimal_sample_result_mid_value) != "null":
            mid_name = list(minimal_sample_result_mid_value.keys())[0]
            self.cluster_connections[cluster_name] = cluster_instance
            self.real_cluster_names[cluster_name] = real_cluster_name
            self.cluster_to_sample_connections[cluster_name] = mid_name
            self.samples[mid_name] = minimal_sample_result_mid_value
            self.numbers[mid_name] = number
        else:
            self.cluster_connections[cluster_name] = cluster_instance
            self.real_cluster_names[cluster_name] = real_cluster_name
            self.samples[cluster_name] = cluster_instance
            self.numbers[cluster_name] = number


    def reducer_final(self):
        print('Reducer')
        changed_clusters = dict()

        categorization_cluster_dict = dict()
        for cluster_dict in self.cluster_connections.values():
            min_distance = float('inf')
            cluster = list(cluster_dict.values())[0]
            cluster_name = list(cluster_dict.keys())[0]
            for sample_name, sample_dict in self.samples.items():
                if sample_dict is not None:
                    sample = list(sample_dict.values())[0]
                    distance = self.evaluate_cosine_weight(cluster, sample)
                    if distance < min_distance:
                        no = False
                        for name, dict_sample in categorization_cluster_dict.items():
                            if sample_dict == dict_sample['sample']:
                                no = True
                        if not no:
                            min_distance = distance
                            if cluster_name not in categorization_cluster_dict:
                                categorization_cluster_dict[cluster_name] = dict()
                            categorization_cluster_dict[cluster_name]['dist'] = distance
                            categorization_cluster_dict[cluster_name]['sample'] = sample_dict

        repeat = dict()
        with open(save_path + '/clusters' + str(self.options.iteration) + '.txt', "w", encoding="utf-8") as f:
            for index, cluster_dict in enumerate(self.cluster_connections.values()):
                cluster_name = list(cluster_dict.keys())[0]
                cluster = list(cluster_dict.values())[0]

                # C\tOLD_CLUSTER_NAME\tOLD_CLUSTER_DATA, NEW_CLUSTER_NAME\tNEW_CLUSTER_DATA
                if cluster_name in categorization_cluster_dict:
                    changed_cluster = dict()
                    changed_cluster[cluster_name] = cluster
                    previous_sample_name = list(categorization_cluster_dict[cluster_name]['sample'].keys())[0]
                    # changed cluster will be added to replace record with previous cluster from data
                    changed_clusters[previous_sample_name] = changed_cluster
                    # previous - new cluster
                    #f.write("C\t" + cluster_name + "\t" + json.dumps(cluster) + "\t" +
                    #  list(self.samples[min_sample_index].keys())[0] + "\t" + json.dumps(
                    #    list(self.samples[min_sample_index].values())[0]) + "\n")
                    # prints replacement for previous cluster - new observed cluster
                    repeat[previous_sample_name] = previous_sample_name
                    yield (index, 'deleted', len(self.cluster_connections.values())), (cluster_name + "\t" + json.dumps(cluster) + '\t' + previous_sample_name + "\t" + json.dumps(
                        list(categorization_cluster_dict[cluster_name]['sample'].values())[0]))
                    #f.write("C\t" + previous_sample_name + "\t" + json.dumps(
                    #    list(categorization_cluster_dict[cluster_name]['sample'].values())[0]) + "\n")
                    f.write("C\t" + cluster_name + "\t" + json.dumps(
                        list(categorization_cluster_dict[cluster_name]['sample'].values())[0]) + "\t" + previous_sample_name +  "\n")
                    del categorization_cluster_dict[cluster_name]
                else:
                    #if cluster_name not in self.cluster_to_sample_connections or \
                    #        self.cluster_to_sample_connections[cluster_name] not in categorization_dict:
                    # previous - previous cluster
                    #f.write("C\t" + cluster_name + "\t" + json.dumps(cluster) + '\t' +
                    #        cluster_name + "\t" + json.dumps(cluster) + "\n")
                    # prints unchanged cluster to file too
                    #yield index, (cluster_name, cluster_name)
                    yield (index, 'no'), (cluster_name + "\t" + json.dumps(cluster) + '\t')
                    f.write("C\t" + cluster_name + "\t" + json.dumps(cluster) + "\t" + self.real_cluster_names[cluster_name] + "\n")

        if int(self.options.iteration) == 1:
            previous_data_file_path = self.get_base_path()
            actual_data_file_path = self.get_data_file_path(1)
        else:
            previous_data_file_path = self.get_data_file_path(int(self.options.iteration) - 1)
            actual_data_file_path = self.get_data_file_path(int(self.options.iteration))

        with open(previous_data_file_path, "r", encoding="utf-8") as previous_file:
            with open(actual_data_file_path, "w", encoding="utf-8") as actual_file:
                for previous_file_line in previous_file:
                    parsed_line = previous_file_line.split('\t')
                    if parsed_line[1] in changed_clusters:
                        new_cluster = changed_clusters[parsed_line[1]]
                        new_cluster_name = list(new_cluster.keys())[0]
                        new_cluster_data = list(new_cluster.values())[0]
                        actual_file.write("S\t" + parsed_line[1] + '\t' + json.dumps(new_cluster_data) + "\t" + self.real_cluster_names[new_cluster_name].replace('\n', '') + '\n')
                        #actual_file.write("S\t" + new_cluster_name + '\t' + json.dumps(new_cluster_data) + '\n')
                        del changed_clusters[parsed_line[1]]
                        yield 's created', (new_cluster_name + "\t" + json.dumps(new_cluster_data))
                    else:
                        actual_file.write("S\t" + parsed_line[1] + '\t' + parsed_line[2].replace('\n', '') + "\t" + parsed_line[1].replace('\n', '') + '\n')
        self.cluster_to_sample_connections = dict()
        self.cluster_connections = dict()
        self.samples = dict()
        print('END')

    @staticmethod
    def create_actualized_data_file(previous_data_file_path: str, actual_data_file_path: str, mapping_dict: dict):
        with open(previous_data_file_path, "r", encoding="utf-8") as previous_file:
            with open(actual_data_file_path, "w", encoding="utf-8") as actual_file:
                for previous_file_line in previous_file:
                    parsed_line = previous_file_line.split('\t')
                    if parsed_line[1] in mapping_dict:
                        new_cluster = mapping_dict[parsed_line[1]]
                        new_cluster_name = list(new_cluster.keys())[0]
                        new_cluster_data = list(new_cluster.values())[0]
                        #actual_file.write("S\t" + new_cluster_name + '\t' + json.dumps(new_cluster_data) + '\n')
                        del mapping_dict[parsed_line[1]]
                        yield 's created', (new_cluster_name + "\t" + json.dumps(new_cluster_data))

                    else:
                        actual_file.write("S\t" + parsed_line[1] + '\t' + parsed_line[2].replace('\n', '') + '\n')

    def steps(self):
        JOBCONF_STEP = {
            'stream.num.map.output.key.fields': '1'
        }
        return [
            MRStep(jobconf=JOBCONF_STEP,
                   mapper_init=self.mapper_init, mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer,
                   reducer_final=self.reducer_final)
        ]


def run_job(MRJobClass, argsArr, loc='local'):
    if loc == 'emr':
        argsArr.extend(['-r', 'emr'])
    print("starting %s job on %s" % (MRJobClass.__name__, loc))
    mrJob = MRJobClass(args=argsArr)
    runner = mrJob.make_runner()
    runner.run()
    print("finished %s job" % MRJobClass.__name__)
    return mrJob, runner


def file_data_are_same(cluster_file1: str, cluster_file2: str):
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


def kmedoid():
    remove_old = True
    base_path = save_path
    previous_data_file_path = save_path + '/dataonly.txt'
    previous_cluster_file_path = save_path + '/clusteronly.txt'
    print("Starting iteration: 1")
    run_job(KMedoid, [
        base_path,
        '-r=hadoop',
        '--output-dir=/temp/result', '--iteration=1'])
 


def test_deletion_correctness():
    print(file_data_are_same('/temp/InitProcessingResults/clusters1.txt', '/temp/InitProcessingResults/clusters2.txt'))
    print(file_data_are_same('/temp/InitProcessingResults/clusters1.txt', '/temp/InitProcessingResults/clusters.txt'))


if __name__ == '__main__':
    #  KMedoid.run()  # now new version has an argument with iteration
    kmedoid()
