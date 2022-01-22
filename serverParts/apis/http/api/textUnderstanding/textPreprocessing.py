from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import word_tokenize
import json


try:
    # Separate array with spaces
    from textUnderstanding.wordInfo import WordInfo
except ImportError:
    # Separate array with spaces
    from serverParts.apis.http.api.textUnderstanding.wordInfo import WordInfo


def separate_with_space(array):
    return ' '.join(array)


# Converts string to lower case
def to_lower_case(string):
    return string.lower()


# Tokenize text to tokens (strings divided by white character)
def tokenize_text(string):
    return word_tokenize(string)


class POSTagging:

    # Initialization of lemmatizer
    def __init__(self):
        self.tag_map = defaultdict(lambda: wordnet.NOUN)
        self.tag_map['J'] = wordnet.ADJ
        self.tag_map['V'] = wordnet.VERB
        self.tag_map['R'] = wordnet.ADV
        self.tag_map['N'] = wordnet.NOUN

    # Lemmatize given data, use WordNetLemmatizer - NOT USED because of language restrictions of WordNetLemmatizer
    # data_to_lemmatize         - data which should be lemmatized
    def lemmatization_and_stop_words_removal_from_documents(self, data_to_lemmatize):
        lemmatized_data = []
        for sentence in data_to_lemmatize:
            lemmatized_words = []
            word_lemmatized = WordNetLemmatizer()
            tokenized = word_tokenize(sentence.lower())

            for word, tag in pos_tag(tokenized):

                if word not in stopwords.words('english') and len(word) > 2 and word.isalpha():
                    word_final = word_lemmatized.lemmatize(word, self.tag_map[tag[0]])
                    lemmatized_words.append(word_final)
            lemmatized_data.append(separate_with_space(lemmatized_words))

    # Lemmatization using WordNet lemmatizer - not used because of language restrictions
    def lemmatization_and_stop_words_removal(self, tokenized_text, stop_words_language):
        lemmatized_data = []
        lemmatized_words = []
        word_lemmatized = WordNetLemmatizer()

        for word, tag in pos_tag(tokenized_text):
            print(word + " " + self.tag_map[tag[0]])
            if word not in stopwords.words(stop_words_language) and len(word) > 2 and word.isalpha():
                word_final = word_lemmatized.lemmatize(word, self.tag_map[tag[0]])
                lemmatized_words.append(word_final)
        lemmatized_data.append(separate_with_space(lemmatized_words))
        # print(lemmatized_data)
        return lemmatized_data

    # Lemmatization with loading stop words from file before lemmatization
    # tokenized_text            - text which is tokenize and prepared for lemmatization
    # stop_words_language_file  - file name which contains  stop words
    def lemmatization_and_stop_words_removal_not_included(self, tokenized_text, stop_words_language_file):

        with open(stop_words_language_file, encoding='utf-8') as stop_words_file:
            stop_words_from_file = json.load(stop_words_file)

        return self.lemmatization_and_stop_words_removal_in_array(tokenized_text, stop_words_from_file)

    def lemma_and_pos_of_word(self, word: str, word_lemmatized = WordNetLemmatizer()):
        gen_list = pos_tag([word])
        for word, tag in gen_list:
            word_final = word_lemmatized.lemmatize(word, self.tag_map[tag[0]])
            return word_final, self.tag_map[tag[0]]

    def pos_of_word(self, word: str):
        gen_list = pos_tag([word])
        for word, tag in gen_list:
            return word, self.tag_map[tag[0]]

    # Lemmatization using WordNet lemmatizer - not used because of language restrictions
    def pos_tagging_analysis(self, tokenized_text, stop_words_language):
        processed_text = list()
        word_lemmatized = WordNetLemmatizer()

        for word, tag in pos_tag(tokenized_text):
            print(word + " " + self.tag_map[tag[0]])
            if len(word) > 2:
                pos_result = self.tag_map[tag[0]]
                if pos_result == 'v' or pos_result == 'j':
                    lemma_word = word_lemmatized.lemmatize(word, )
                    pos_processed_word = WordInfo(word)
                    if pos_result == 'v':
                        pos_processed_word.as_verb(lemma_word)
                    elif pos_result == 'j':
                        pos_processed_word.as_adj(lemma_word)
                elif pos_result == 'n':
                    pos_processed_word.as_noun(word)
                processed_text.append(pos_processed_word)

        return processed_text
