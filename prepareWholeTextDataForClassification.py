import os
import json
import np


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_file_content(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
    except UnicodeDecodeError:
        return None
    return "/n".join(content)


def process_text_categories_from_dict(path_to_dict: str):
    contents = list()
    for category_file_name in os.listdir(path_to_dict):
        category_name = category_file_name
        path_to_category_dict = os.path.join(path_to_dict, category_file_name)
        for file_number, file_name in enumerate(os.listdir(path_to_category_dict)):
            file_path = os.path.join(path_to_category_dict, file_name)

            print(file_path)
            file_content = dict()
            file_content["category"] = category_name
            file_content["text"] = load_file_content(file_path)
            contents.append(file_content)
    return contents


if __name__ == '__main__':
    samples = process_text_categories_from_dict("D://dipldatasets/text-categories/base")
    np.random.shuffle(samples)

    save_as_json(samples[-1000:], "text_categories_test.json")
    save_as_json(samples[:-1000], "text_categories_train.json")

