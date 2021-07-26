from rake_nltk import Rake
# from keybert import KeyBERT #ommited for large keybert file and cost for processing
import re


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


def rake_keyword_key_extractor_analysis(text, content_dictionary=None):
    if content_dictionary is None:
        content_dictionary = dict()
    rake = Rake()
    rake.extract_keywords_from_text(text)
    content_dictionary['rake'] = filtering_condition_for_words(rake.get_ranked_phrases())
    return content_dictionary


def keyber_keyword_extractor_analysis(text, content_dictionary=None, keyphrase_range=(1, 2), language="english"):
    if content_dictionary is None:
        content_dictionary = dict()
    # keybert = KeyBERT('distilbert-base-nli-mean-tokens')
    # content_dictionary['keybert'] = keybert.extract_keywords(text,
    # keyphrase_ngram_range=keyphrase_range, stop_words=language)
    return content_dictionary


def analyze_keywords(text, analyze_methods=None, keyphrase_range=(1, 2), language='english'):
    content_dictionary = dict()
    if analyze_methods is None or 'rake' in analyze_methods:
        content_dictionary = rake_keyword_key_extractor_analysis(text, content_dictionary)
    if analyze_methods is None or 'keybert' in analyze_methods:
        content_dictionary = keyber_keyword_extractor_analysis(text, content_dictionary, keyphrase_range, language)
    return content_dictionary
