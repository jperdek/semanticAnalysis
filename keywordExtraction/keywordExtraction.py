from rake_nltk import Rake
from keybert import KeyBERT
import json
import re


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def filtering_condition_for_words(array_words):
    new_word_array = []
    for word in array_words:
        if len(word) <= 3:
            continue
        if len(re.findall(r"^[0-9]*$", word)) > 0:
            continue
        if len(re.findall(r"[0-9]+[^0-9 ]+[0-9]+", word)) > 0:
            continue
        if len(re.findall(r"^[?&%^*)_($#@.!,'\\\/\"-]*$", word)) > 0:
            continue
        if len(re.findall('[0-9]+[a-zA-Z\\\\]+', word)) > 0:
            continue
        new_word_array.append(word)
    return new_word_array


def rake_keyword_extractor(filename):
    rake = Rake()
    extractor_data = load_as_json(filename)
    categories = dict()
    result_dict = dict()
    for content in extractor_data:
        if content['category'] not in categories:
            categories[content['category']] = []
            result_dict[content['category']] = []
        categories[content['category']].append(content['text'])
    for category, categoryArray in categories.items():
        print(category)
        rake.extract_keywords_from_sentences(categoryArray)
        word_array = filtering_condition_for_words(rake.get_ranked_phrases())
        print(len(word_array))
        result_dict[category] = word_array
    return result_dict


def keybert_keyword_extractor(filename, keyphrase_range=(1, 2)):
    model = KeyBERT('distilbert-base-nli-mean-tokens')
    extractor_data = load_as_json(filename)
    categories = dict()
    result_dict = dict()
    for content in extractor_data:
        if content['category'] not in categories:
            categories[content['category']] = []
            result_dict[content['category']] = []
        categories[content['category']].append(content['text'])
    for category, category_array in categories.items():
        print(category)
        word_set = set()
        for text_from_category in category_array:
            keywords = model.extract_keywords(text_from_category, keyphrase_ngram_range=keyphrase_range,
                                              stop_words='english')
            for keyword, value in keywords:
                word_set.add(keyword)
        word_array = list(word_set)
        print(len(word_array))
        result_dict[category] = word_array
    return result_dict


def rake_keyword_extractor_raw_text(filename):
    rake = Rake()
    word_array = list()
    with open(filename, "r", encoding="utf-8") as file:
        try:
            extractor_data = file.readlines()
            rake.extract_keywords_from_sentences(extractor_data)
            word_array = filtering_condition_for_words(rake.get_ranked_phrases())
        except UnicodeDecodeError:
            print("Cant extract data from file: " + filename)
    return word_array


def keybert_keyword_extractor_raw_text(filename, keyphrase_range=(1, 2)):
    model = KeyBERT('distilbert-base-nli-mean-tokens')
    word_set = set()
    word_array = list()
    with open(filename, "r", encoding="utf-8") as file:
        try:
            extractor_data = file.readlines()
            keywords = model.extract_keywords(extractor_data, keyphrase_ngram_range=keyphrase_range,
                                              stop_words='english')
            for record in keywords:
                for record_part in record:
                    if record_part != 'None Found':
                        for position, part in enumerate(record_part):
                            if position == 0:
                                word_set.add(part)
                            elif position > 1:
                                print("Error: position is greater then 1: ")
                                print(part)
                    elif record_part == 'None Found':
                        # print("Not found")
                        pass
                    else:
                        print("Error: problem occurred record is: ")
                        print(record_part)
            word_array = list(word_set)

        except UnicodeDecodeError:
            print("Cant extract data from file: " + filename)
        except ValueError as e:
            print("Error: Value error: ")
            print(e)
    return word_array


if __name__ == "__main__":
    #  result_rake_dict = rake_keyword_extractor("../pageAnalyser/CETD/extractor.json")
    result_keybert_dict = keybert_keyword_extractor("../pageAnalyser/CETD/extractor.json", (1, 1))
    save_as_json(result_keybert_dict, 'keybert_CETD_extrctor.json')
    # save_as_json(result_rake_dict, 'rake_CETD_extrctor_word.json')