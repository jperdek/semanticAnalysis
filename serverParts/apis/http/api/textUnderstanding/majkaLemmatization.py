#from majka import Majka
import sys
import json


# Lemmatizer class to provide lemmatization base on Czech project Majka
class MajkaLemmatization:

    # Initialization of lemmatizer
    def __init__(self):
        self.chosen_majkas = []
        self.majka = None

    # Initializes majka for lemmatization
    # language_shortening       - base language in which lemmatization should be provided
    def majka_init_for_lemmatization(self, language_shortening):
        majka_paths = self.load_majka_paths('./majka/majka_file_paths.json')

        if language_shortening not in majka_paths.keys():
            print("Unrecognized language for Majka! "+str(majka_paths))
            sys.exit(2)

        #self.majka = Majka(majka_paths[language_shortening])
        self.majka.first_only = True
        self.majka.tags = False

    # Initializes array of majka instances for given languages
    # language_shortenings      - languages to be lammatized by majka
    def all_chosen_majkas_init_for_lemmatization(self, language_shortenings):
        majka_paths = self.load_majka_paths('./majka/majka_file_paths.json')

        for language_shortening in language_shortenings:
            if language_shortening not in majka_paths.keys():
                print("Unrecognized language for Majka! " + str(majka_paths))
                sys.exit(2)

            #majka = Majka(majka_paths[language_shortening])
            #majka.first_only = True
            #majka.tags = False
            #self.chosen_majkas.append(majka)

    # Loads majka configuration JSON file
    # file      - file to be loaded
    @staticmethod
    def load_majka_paths(file):
        with open(file, encoding='utf-8') as majka_paths:
            return json.load(majka_paths)

    # Separate array with spaces
    @staticmethod
    def separate_with_space(array):
        return ' '.join(array)
    
    # tokenized_text            - text which is tokenize and prepared for lemmatization
    # stop_words_language_file  - file name which contains  stop words
    def lemmatization_and_stop_words_removal_in_array(self, tokenized_text, stop_words_from_file):
        lemmatized_words = []

        for word in tokenized_text:
            # print(word)
            if word not in stop_words_from_file and len(word) > 2 and word.isalpha():
                word_final = self.majka.find(word)  # word_Lemmatized.lemmatize(word, self.tag_map[tag[0]])
                if len(word_final) > 0:
                    lemmatized_words.append(word_final[0]['lemma'])

        return MajkaLemmatization.separate_with_space(lemmatized_words)

    # tokenized_text            - text which is tokenize and prepared for lemmatization
    # stop_words_language_file  - file name which contains  stop words
    def lemmatization_and_stop_words_removal_in_array_all_majka(self, tokenized_text, stop_words_from_file):
        lemmatized_words = []

        for word in tokenized_text:
            # print(word)
            if word not in stop_words_from_file and len(word) > 2 and word.isalpha():
                for majka in self.chosen_majkas:
                    word_final = majka.find(word)  # word_Lemmatized.lemmatize(word, self.tag_map[tag[0]])
                    if len(word_final) > 0:
                        lemmatized_words.append(word_final[0]['lemma'])

        return MajkaLemmatization.separate_with_space(lemmatized_words)

    # tokenized_text            - text which is tokenize and prepared for lemmatization
    # stop_words                - stop words array in language of tokenized text
    def lemmatization_and_loaded_stop_words_removal_in_array(self, tokenized_text, stop_words):
        lemmatized_words = []

        for word in tokenized_text:
            if word not in stop_words and len(word) > 2 and word.isalpha():
                word_final = self.majka.find(word)  # word_Lemmatized.lemmatize(word, self.tag_map[tag[0]])

                if len(word_final) > 0:
                    lemmatized_words.append(word_final[0]['lemma'])

        return MajkaLemmatization.separate_with_space(lemmatized_words)