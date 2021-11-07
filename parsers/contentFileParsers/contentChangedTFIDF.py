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


def process_text_categories_from_dict(path_to_dict: str, save_separately: bool = True, clear_after_files: int = 200):
    indexes = dict()
    for category_file_name in os.listdir(path_to_dict):
        if save_separately:
            indexes = dict()
        category_name = category_file_name
        path_to_category_dict = os.path.join(path_to_dict, category_file_name)
        for file_number, file_name in enumerate(os.listdir(path_to_category_dict)):
            file_path = os.path.join(path_to_category_dict, file_name)
            print(file_path)
            content = load_file_content(file_path)
            if not content:
                continue
            # indexing.index_words_term_freq_doc_freq_for_category(indexes, content, category_name)
            indexing.index_words_term_freq_doc_freq_for_category(indexes, content, category_name)
            if file_number % clear_after_files == 0:
                print("cleaning")
                indexing.remove_index_words_term_freq_doc_freq_for_category(indexes[category_name])
        indexing.remove_index_words_term_freq_doc_freq_for_category(indexes[category_name])
        indexing.count_changed_tfidf_info(indexes[category_name])
        if save_separately:
            save_as_json(indexes[category_name], "../../output/changed_tfidf/index-cat-" + category_name + ".json")
        #indexing.count_tf_idf(content, indexes)
    return indexes


def process_text_categories():
    result_index = process_text_categories_from_dict("D://dipldatasets/text-categories/base", True)
    save_as_json(merge_text_categories(), "../../output/index-cat-all.json")


def merge_text_categories(category_path: str = "../../output/changed_tfidf"):
    merged_result = dict()
    for extended_file_name in os.listdir(category_path):
        file_name = extended_file_name[extended_file_name.rfind("-") + 1:extended_file_name.rfind(".json")]
        resulting_file_name = os.path.join(category_path, extended_file_name)
        merged_result[file_name.lower()] = load_as_json(resulting_file_name)
    return merged_result


if __name__ == "__main__":
    process_text_categories()