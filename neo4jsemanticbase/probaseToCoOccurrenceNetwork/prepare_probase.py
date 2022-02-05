import json


def save_as_json(object_to_save: any, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_Unique_names(file_name: str, unique_names: dict) -> None:
    number_lines = 0
    with open(file_name, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            if index % 100000 == 0:
                print(index)
            number_lines = number_lines + 1

            text1, text2, value = line.split('\t')

            unique_names[text1] = "1"
            unique_names[text2] = "2"

    print("Whole length: " + str(len(unique_names)))


def load_values(file_name: str, result_dict: dict) -> None:
    number_lines = 0
    with open(file_name, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            if index % 100000 == 0:
                print(index)
            number_lines = number_lines + 1

            text1, text2, value = line.split('\t')

            if text2 not in result_dict:
                result_dict[text2] = dict()

            result_dict[text2][text1] = float(value)
    print("Whole length: " + str(len(result_dict)))


def save_to_jsonld(file_name: str, result_dict) -> None:
    with open(file_name, "w", encoding="utf-8") as file:
        for concept_name, data in result_dict.items():
            file.write(concept_name + "\t" + json.dumps(data) + "\n")


if __name__ == "__main__":
    concept_vectors = dict()
    entities = dict()
    load_Unique_names("D://dipldatasets/data-concept-instance-relations.txt", entities)
    save_as_json(list(entities.keys()), "probase_entities.json")
    entities = None
    load_values("D://dipldatasets/data-concept-instance-relations.txt", concept_vectors)
    save_to_jsonld("optimized_probase.txt", concept_vectors)
