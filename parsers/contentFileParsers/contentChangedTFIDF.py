import json
import os
import parsers.token_indexing as indexing


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_file_content(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
    except UnicodeDecodeError:
        return None
    return "/n".join(content)


def process_text_categories_from_dict(path_to_dict: str):
    indexes = dict()
    doc_freq_index = dict()
    for category_file_name in os.listdir(path_to_dict):
        category_name = category_file_name
        path_to_category_dict = os.path.join(path_to_dict, category_file_name)
        for file_name in os.listdir(path_to_category_dict):
            file_path = os.path.join(path_to_category_dict, file_name)
            print(file_path)
            content = load_file_content(file_path)
            if not content:
                continue
            # indexing.index_words_term_freq_doc_freq_for_category(indexes, doc_freq_index, content, category_name)
            indexing.index_words_term_freq_doc_freq_for_category(indexes, doc_freq_index, content, category_name)
        indexing.remove_index_words_term_freq_doc_freq_for_category(indexes[category_name])
        indexing.count_changed_tfidf_info(indexes[category_name])
        indexing.count_tf_idf(content, indexes)
        break
    return indexes


def process_text_categories():
    result_index = process_text_categories_from_dict("D://dipldatasets/text-categories/base")
    save_as_json(result_index, "../../output/index-cat.json")


if __name__ == "__main__":
    process_text_categories()