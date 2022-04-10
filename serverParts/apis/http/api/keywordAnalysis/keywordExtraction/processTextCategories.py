import os
import keywordExtraction


def extraction_chooser(extraction_type: str, filename: str):
    if extraction_type == "RAKE":
        return keywordExtraction.rake_keyword_extractor_raw_text(filename)
    elif extraction_type == "KEYBERT":
        return keywordExtraction.keybert_keyword_extractor_raw_text(filename)


def process_text_categories_from_dict(path_to_dict: str, extraction_type: str):
    result_dict = dict()
    for category_file_name in os.listdir(path_to_dict):
        category_name = category_file_name
        result_dict[category_name] = list()
        path_to_category_dict = os.path.join(path_to_dict, category_file_name)
        if category_name not in result_dict:
            result_dict[category_name] = []
        for file_name in os.listdir(path_to_category_dict):
            file_path = os.path.join(path_to_category_dict, file_name)
            print(file_path)
            result_dict[category_name] = result_dict[category_name] + extraction_chooser(extraction_type, file_path)
        keywordExtraction.save_as_json(result_dict[category_name], "./processed/text-categories-keybert-" + category_file_name + ".json")
    return result_dict


def process_text_categories():
    # result = process_text_categories_from_dict("D://dipldatasets/text-categories/base", "RAKE")
    # keywordExtraction.save_as_json(result, "./processed/text-categories-rake.json")
    result = process_text_categories_from_dict("D://dipldatasets/text-categories/base", "KEYBERT")
    keywordExtraction.save_as_json(result,
                                   "../../../../../../output/keywordExtraction/processed/text-categories-keybert.json")


if __name__ == "__main__":
    process_text_categories()
