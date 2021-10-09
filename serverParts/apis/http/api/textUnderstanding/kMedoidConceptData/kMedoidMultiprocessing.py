import numpy as np
import math
import random
import sys
import json
import multiprocessing


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

            if text1 in result_dict[text2]:
                print("Error: text1 included")
            # text2 is a concept (text1 is only concept instance)
            # text1 is its instance with given distribution - as associated value in vector
            if len(result_dict.keys()) > 10000:
                result_dict[text2][text1] = value
                break
            else:
                result_dict[text2][text1] = value
            if number_lines > 10000000:
                print('breaking')
                break

            if number_lines % 1000000 == 0:
                # number_lines = 0
                print(1000000)
            # if len(result_dict[text2].keys()) > 50:
            #    continue

    # print(len(result_dict[text2].keys()))
    print("Whole length: " + str(len(result_dict)))
    # print(result_dict[text2].keys())


def evaluate_cosine_weight(dict_vector1, dict_vector2) -> float:
    unique_keys = np.unique(list(dict_vector1.keys()) + list(dict_vector2.keys()))
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
    return 1.0 - upper_value / (0.0 + bottom_value_vector1 * bottom_value_vector2)


def count_minimal_distance_for_sample_on_medoids(point_to_associate_key: str,
                                                 random_k_sample_keys: list,
                                                 result_dict: dict,
                                                 result_connections: dict,
                                                 chosen_sample_key: str,
                                                 chosen_medoid_sample_key: str,
                                                 distance: dict):
    minimal_distance = None
    closest_medoid_key = None

    for chosen_medoid_key in random_k_sample_keys:
        calculated_value = evaluate_cosine_weight(result_dict[point_to_associate_key], result_dict[chosen_medoid_key])

        if minimal_distance is None or minimal_distance < calculated_value:
            minimal_distance = calculated_value
            closest_medoid_key = chosen_medoid_key

    if minimal_distance is not None and result_connections[chosen_sample_key]['dist'] > minimal_distance:
        result_connections[chosen_sample_key]['nmedoid'] = closest_medoid_key
        result_connections[chosen_sample_key]['ndist'] = minimal_distance
        distance["new"] = 0.0 + distance["new"] + minimal_distance
    else:
        result_connections[chosen_sample_key]['nmedoid'] = result_connections[chosen_medoid_sample_key]['medoid']
        result_connections[chosen_sample_key]['ndist'] = result_connections[chosen_sample_key]['dist']
        distance["new"] = 0.0 + distance["new"] + result_connections[chosen_sample_key]['dist']


def count_minimal_distance_for_sample_on_medoids_with_insert(point_to_associate_key: str,
                                                             random_k_sample_keys: list,
                                                             result_dict: dict,
                                                             result_connections: dict,
                                                             distance: dict):
    minimal_distance = None
    closest_medoid_key = None

    for chosen_medoid_key in random_k_sample_keys:
        calculated_value = evaluate_cosine_weight(result_dict[point_to_associate_key], result_dict[chosen_medoid_key])

        distance['previous'] = distance['previous'] + calculated_value
        if minimal_distance is None or minimal_distance < calculated_value:
            minimal_distance = calculated_value
            closest_medoid_key = chosen_medoid_key

    result_connections[point_to_associate_key]['medoid'] = closest_medoid_key
    result_connections[point_to_associate_key]['dist'] = minimal_distance


def count_minimal_distance_for_sample_on_medoids_without_medoid(point_to_associate_key: str,
                                                                chosen_medoid_sample_key: str,
                                                                random_k_sample_keys: list,
                                                                result_dict: dict):
    minimal_distance = None
    closest_medoid_key = None

    for chosen_medoid_key in random_k_sample_keys:
        if chosen_medoid_key != chosen_medoid_sample_key:
            calculated_value = evaluate_cosine_weight(result_dict[point_to_associate_key],
                                                      result_dict[chosen_medoid_key])

            if minimal_distance is None or minimal_distance < calculated_value:
                minimal_distance = calculated_value
                closest_medoid_key = chosen_medoid_key
    return closest_medoid_key, minimal_distance


def count_distance(point_to_associate_key: str,
                   chosen_sample_key: str,
                   chosen_medoid_sample_key: str,
                   random_k_sample_keys: list,
                   result_dict: dict,
                   result_connections: dict,
                   distance: dict
                   ):
    minimal_distance = None
    closest_medoid_key = None

    if point_to_associate_key not in random_k_sample_keys and chosen_sample_key != point_to_associate_key:
        if result_connections[point_to_associate_key]['medoid'] == chosen_medoid_sample_key:
            closest_medoid_key, minimal_distance = count_minimal_distance_for_sample_on_medoids_without_medoid(
                point_to_associate_key, chosen_medoid_sample_key, random_k_sample_keys, result_dict)

        calculated_value = evaluate_cosine_weight(result_dict[point_to_associate_key],
                                                  result_dict[chosen_sample_key])

        if minimal_distance is None or minimal_distance < calculated_value:
            minimal_distance = calculated_value
            closest_medoid_key = chosen_sample_key

    if minimal_distance is not None and result_connections[point_to_associate_key]['dist'] > minimal_distance:
        result_connections[point_to_associate_key]['nmedoid'] = closest_medoid_key
        result_connections[point_to_associate_key]['ndist'] = minimal_distance
        distance["new"] = 0.0 + distance["new"] + minimal_distance
    else:
        result_connections[point_to_associate_key]['nmedoid'] = result_connections[point_to_associate_key]['medoid']
        result_connections[point_to_associate_key]['ndist'] = result_connections[point_to_associate_key]['dist']
        distance["new"] = 0.0 + distance["new"] + \
                          result_connections[point_to_associate_key]['dist']


def associate_medoids_to_closest_one(random_k_sample_keys: list,
                                     result_dict: dict,
                                     pool: multiprocessing.Pool,
                                     manager: multiprocessing.Manager,
                                     distance: dict) -> dict:
    result_connections = manager.dict()
    distance['previous'] = 0
    number_done = 0

    for chosen_medoid_key in random_k_sample_keys:
        result_connections[chosen_medoid_key] = dict()
        result_connections[chosen_medoid_key]['medoid'] = chosen_medoid_key

    for point_to_associate_key in result_dict.keys():
        # point is not chosen to be medoid

        if point_to_associate_key not in random_k_sample_keys:
            result_connections[point_to_associate_key] = manager.dict()
            pool.apply_async(
                count_minimal_distance_for_sample_on_medoids_with_insert,
                (point_to_associate_key, random_k_sample_keys, result_dict, result_connections, distance))
        else:
            result_connections[point_to_associate_key] = manager.dict()
            result_connections[point_to_associate_key]['medoid'] = point_to_associate_key
            result_connections[point_to_associate_key]['dist'] = 0

            # if result_connections[point_to_associate_key]['medoid'] is None:
            #    print("Error: medoid cant be None: " + point_to_associate_key)

        number_done = number_done + 1
        if number_done % 100000 == 0:
            print("Done is: " + str(number_done / len(result_dict.keys())))
    return result_connections


def recompute_swap_for_medoid(chosen_sample_key: str,
                              chosen_medoid_sample_key: str,
                              random_k_sample_keys: list,
                              result_dict: dict,
                              result_connections: dict,
                              distance: dict,
                              pool: multiprocessing.Pool) -> float:
    keys = result_dict.keys()
    distance["new"] = 0.0
    for point_to_associate_key in keys:
        # point is not chosen to be medoid
        pool.apply_async(count_distance, (point_to_associate_key,
                                          chosen_sample_key,
                                          chosen_medoid_sample_key,
                                          random_k_sample_keys,
                                          result_dict,
                                          result_connections,
                                          distance))

    pool.apply_async(
        count_minimal_distance_for_sample_on_medoids,
        (chosen_medoid_sample_key,
         random_k_sample_keys,
         result_dict,
         result_connections,
         chosen_sample_key,
         chosen_medoid_sample_key,
         distance)).get()

    if distance["new"] < distance["previous"]:
        previous = distance['previous']
        distance['previous'] = distance["new"]
        random_k_sample_keys.remove(chosen_medoid_sample_key)
        random_k_sample_keys.append(chosen_sample_key)
        for result_connection_key in result_connections.keys():
            result_connections[result_connection_key]['medoid'] = result_connections[result_connection_key]['nmedoid']
            result_connections[result_connection_key]['dist'] = result_connections[result_connection_key]['ndist']
        return previous - distance["new"]
    return distance["previous"] - distance["new"]


def try_swap_medoids(random_k_sample_keys: list, result_dict: dict, result_connections: dict):
    for point_to_associate_key in result_dict.keys():
        if point_to_associate_key not in random_k_sample_keys:
            for chosen_medoid_key in random_k_sample_keys:
                if recompute_swap_for_medoid(point_to_associate_key, chosen_medoid_key,
                                             random_k_sample_keys, result_dict, result_connections) > 0:
                    pass


def create_random_array(length: int) -> list:
    array = list(range(0, length))
    for i in range(0, length):
        position = random.randrange(i, length)
        pom = array[position]
        array[position] = array[i]
        array[i] = pom
    return array


def try_swap_medoids_randomized(random_k_sample_keys: list, result_dict: dict, result_connections: dict,
                                distance: dict, pool: multiprocessing.Pool,
                                iterations: int = 1000, treshold: float = 1000) -> bool:
    array = create_random_array(len(result_dict.keys()) * len(random_k_sample_keys))
    k = len(random_k_sample_keys)
    min_value = distance['previous']

    for iteration, array_value in enumerate(array):
        point_to_associate_key = list(result_dict.keys())[int(array_value / k)]
        chosen_medoid_key = random_k_sample_keys[array_value % k]
        value = recompute_swap_for_medoid(point_to_associate_key, chosen_medoid_key,
                                          random_k_sample_keys, result_dict, result_connections, distance, pool)
        if iteration % 10 == 0:
            print("DIstance: " + str(distance['previous']))

        if distance['previous'] < min_value:
            min_value = distance['previous']
            counter = 0
        else:
            counter = counter + 1

        if counter == 100 or (0.0 < value < 1.0):
            return False
        # if iteration > iterations:
        #    return False
    return False


def print_results(result_connections: dict) -> None:
    sorted(result_connections.items(), key=lambda x: x[1]['medoid'])
    for result_connection_key in result_connections.keys():
        print(result_connections[result_connection_key]['medoid'] + " --> " + result_connection_key)


def save_as_json(data: dict, file_name: str):
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(json.dumps(data))


def save_results(result_connections: dict, file_name) -> None:
    medoids = dict()
    for result_connection_key in result_connections.keys():
        if result_connections[result_connection_key]['medoid'] not in medoids:
            medoids[result_connections[result_connection_key]['medoid']] = list()
        medoids[result_connections[result_connection_key]['medoid']].append(result_connection_key)
    save_as_json(medoids, file_name)


def k_medoid_algorithm_multiprocess(k: int, result_dict: dict,
                                    max_iterations: int = 1000, treshold: float = 1000,
                                    file_name: str = "group.json") -> None:
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    print(multiprocessing.cpu_count())
    manager = multiprocessing.Manager()
    distance = manager.dict()
    random_k_medoids_keys = random.sample(result_dict.keys(), k)
    print("Initial asociation of medoids started:")
    result_connections = associate_medoids_to_closest_one(random_k_medoids_keys, result_dict, pool, manager, distance)
    print(len(result_dict.keys()))
    print("Swaping medoids started:")
    try_swap_medoids_randomized(random_k_medoids_keys, result_dict, result_connections, distance,
                                pool, max_iterations, treshold)
    # print_results(result_connections)
    print("Saving results")
    save_results(result_connections, file_name)
    print("Closing pool")
    pool.close()
    print("Joining treads")
    pool.join()


if __name__ == "__main__":
    main_result_dict = dict()
    load_values('D://dipldatasets/data-concept-instance-relations.txt', main_result_dict)
    k_medoid_algorithm_multiprocess(2000, main_result_dict, 1000, 0.05)
