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


def keybert_keyword_extractor(filename):
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
            keywords = model.extract_keywords(text_from_category, keyphrase_ngram_range=(1, 2), stop_words='english')
            for keyword, value in keywords:
                word_set.add(keyword)
        word_array = list(word_set)
        print(len(word_array))
        result_dict[category] = word_array
    return result_dict


# rake_keyword_extractor("./pageAnalyser/CETD/extractor.json")
result_keybert_dict = keybert_keyword_extractor("./pageAnalyser/CETD/extractor.json")
save_as_json(result_keybert_dict, 'keybert_CETD_extrctor.json')
