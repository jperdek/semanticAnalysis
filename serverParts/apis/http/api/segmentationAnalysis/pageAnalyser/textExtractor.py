import json
import os
from bs4 import BeautifulSoup


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def create_dom_beautiful_soup(file_name):
    with open(file_name, "rb") as file:
        parser = BeautifulSoup(file.read().decode('utf-8', 'ignore'), "html.parser")
    return parser


def create_record(category, text, page_name):
    record = dict()
    record['file'] = page_name
    record['category'] = category
    record['text'] = text
    return record


def get_plain_text_beautiful_soup(path_dataset, path_result_json, domain_only=True):
    root = []
    whole_count = 0
    for category in os.listdir(path_dataset):
        print(path_dataset)
        path_category = os.path.join(path_dataset, category)
        if os.path.isdir(path_category):
            for domain in os.listdir(path_category):
                domain_dir = os.path.join(path_category, domain)
                if os.path.isdir(domain_dir):
                    for page_name in os.listdir(domain_dir):
                        page = os.path.join(domain_dir, page_name)
                        try:
                            dom = create_dom_beautiful_soup(page)
                        except UnicodeDecodeError:
                            continue
                        print(page)
                        # print(elementTree.tostring(dom.getroot(), encoding='utf8').decode('utf8'))
                        text = dom.get_text()
                        root.append(create_record(category, text, page_name))
                        whole_count = whole_count + 1
                    if domain_only:
                        save_as_json(root, path_result_json + "_" + domain + ".json")
                        root = dict()
                        whole_count = 0

    if not domain_only:
        save_as_json(root, path_result_json)


def convert_dict_of_files_to_array_of_dict(input_json_file, output_json_file):
    result_conversion = []
    to_process = load_as_json(input_json_file)
    for file_name, content in to_process.items():
        record = dict()
        record['file'] = file_name
        record['category'] = content['category']
        record['text'] = " ".join(content['text'])
        result_conversion.append(record)
    save_as_json(result_conversion, output_json_file)


def convert_document_to_text(html_page, category=None):
    result = dict()
    if category is not None:
        result['category'] = category

    try:
        dom = BeautifulSoup(html_page, "html.parser")
        result['text'] = dom.get_text()
    except UnicodeDecodeError as e:
        result['text'] = "Error: " + str(e)
    return result


if __name__ == "__main__":
    convert_dict_of_files_to_array_of_dict('d:\\dipldatasets\\weir\\output_beautifulsoap.json',
                                           'd:\\dipldatasets\\weir\\output_beautifulsoap_processed.json')
    # get_plain_text_beautiful_soup("d:/dipldatasets/weir/dataset/", "./plain_text.json", False)
