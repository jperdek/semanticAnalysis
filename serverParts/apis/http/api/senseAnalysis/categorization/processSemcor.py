from nltk.corpus import wordnet as ewn
import xml.dom.minidom
import os
from nltk.corpus.reader.wordnet import WordNetError
from nltk.corpus import wordnet
import json


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


# should have WN version (e.g. 3.0)
# Look up a synset given the information from SemCor
def sc2ss(sensekey):
    try:
        return ewn.lemma_from_key(sensekey).synset()
    except WordNetError:
        return None


def process_semcor_dir_xml_files(path_to_files,  word_synset_dict):
    for file_name in os.listdir(path_to_files):
        whole_path = os.path.join(path_to_files, file_name)
        semcor_doc = xml.dom.minidom.parse(whole_path)
        for wf_element in semcor_doc.getElementsByTagName("wf"):
            lexsns = wf_element.getAttribute("lexsn")
            lemma = wf_element.getAttribute("lemma")
            if lexsns is not None and lexsns != "":
                for lexsn in lexsns.split(';'):
                    if lexsn is not None and lexsn != "" and lemma is not None and lemma != "":
                        # print(lemma + '%' + lexsn)
                        ss = sc2ss(lemma + '%' + lexsn)
                        if ss is not None:
                            word_name = wf_element.firstChild.nodeValue
                            synset_name = ss.name()
                            definition = ss.definition()
                            if word_name not in word_synset_dict:
                                word_synset_dict[word_name] = dict()
                            if synset_name not in word_synset_dict[word_name]:
                                word_synset_dict[word_name][synset_name] = dict()
                                word_synset_dict[word_name][synset_name]["count"] = 0
                                word_synset_dict[word_name][synset_name]["definition"] = definition

                            word_synset_dict[word_name][synset_name]['count'] = \
                                word_synset_dict[word_name][synset_name]["count"] + 1
    return word_synset_dict


def process_semcor():
    word_synset_dict = dict()
    word_synset_dict = process_semcor_dir_xml_files("D:/dipldatasets/semcor/brown1/tagfiles", word_synset_dict)
    word_synset_dict = process_semcor_dir_xml_files("D:/dipldatasets/semcor/brown2/tagfiles", word_synset_dict)
    word_synset_dict = process_semcor_dir_xml_files("D:/dipldatasets/semcor/brownv/tagfiles", word_synset_dict)
    word_synset_dict = count_category_word_frequencies(word_synset_dict)
    word_synset_dict = add_and_initialize_category_associations(word_synset_dict,
                                                                "../../../../../../output/domain-lookup/wordnet"
                                                                "/domain-parts.json")
    save_as_json(word_synset_dict, "semcor_frequencies.json")


def count_category_word_frequencies(wordnet_sync_dict):
    for word_name, senses in wordnet_sync_dict.items():
        count = 0
        for sense_info in senses.values():
            count = count + sense_info["count"]
        wordnet_sync_dict[word_name]["count"] = count
    return wordnet_sync_dict


def add_category_associations(word_synset_dict, path_to_wordnet_categories):
    wordnet_categories = load_as_json(path_to_wordnet_categories)
    for wordnet_category, wordnet_subcategories in wordnet_categories.items():
        for wordnet_word in wordnet_subcategories.keys():
            for lemma in wordnet.lemmas(wordnet_word):
                lemma_name = lemma.name()
                lemma_synset = lemma.synset()
                synset_name = lemma_synset.name()
                if lemma_name in word_synset_dict:
                    if synset_name in word_synset_dict[lemma_name]:
                        word_synset_dict[lemma_name][synset_name]["category"] = wordnet_category
                        print(lemma_name, synset_name)
                        if word_synset_dict[lemma_name][synset_name]["definition"] != lemma_synset.definition():
                            print("wrong")
    return word_synset_dict


def add_and_initialize_category_associations(word_synset_dict, path_to_wordnet_categories, no_mapping_count=1):
    wordnet_categories = load_as_json(path_to_wordnet_categories)
    for wordnet_category, wordnet_subcategories in wordnet_categories.items():
        for wordnet_word in wordnet_subcategories.keys():
            for lemma in wordnet.lemmas(wordnet_word):
                lemma_name = lemma.name()
                lemma_synset = lemma.synset()
                synset_name = lemma_synset.name()
                if lemma_name not in word_synset_dict:
                    word_synset_dict[lemma_name] = dict()

                if synset_name not in word_synset_dict[lemma_name]:
                    word_synset_dict[lemma_name][synset_name] = dict()
                    word_synset_dict[lemma_name][synset_name]["count"] = no_mapping_count
                    word_synset_dict[lemma_name][synset_name]["definition"] = lemma_synset.definition()

                word_synset_dict[lemma_name][synset_name]["category"] = wordnet_category
                print(lemma_name, synset_name)
                if word_synset_dict[lemma_name][synset_name]["definition"] != lemma_synset.definition():
                    print("wrong")
    return word_synset_dict


def create_statistics_from_semcor_and_categories(path_to_word_synset_dict):
    word_synset_dict = load_as_json(path_to_word_synset_dict)
    number_words = 0
    category_not_found = 0
    count_limit = []
    all_words_with_senses = 0
    max_count = -1
    min_count = 1000000000
    for i in range(0, 100):
        count_limit.append(0)
    for word, word_senses in word_synset_dict.items():
        number_words = number_words + 1
        number_word_senses = 0
        for word_sense, word_sense_info in word_senses.items():
            if word_sense != "count":
                number_word_senses = number_word_senses + 1
                if "category" not in word_sense_info:
                    category_not_found = category_not_found + 1
                if word_sense_info["count"] < 100:
                    count_limit[word_sense_info["count"]] = count_limit[word_sense_info["count"]] + 1
                if word_sense_info["count"] > max_count:
                    max_count = word_sense_info["count"]
                if word_sense_info["count"] < min_count:
                    min_count = word_sense_info["count"]
        all_words_with_senses = all_words_with_senses + number_word_senses

    print("Number words: ", number_words)
    print("Number meanings: ", all_words_with_senses)
    print("Meanings without categories set: ", category_not_found)
    print("Average number meanings: ", all_words_with_senses / number_words)
    print("Min count: ", min_count)
    print("Max count: ", max_count)
    for i in range(0, 100):
        print("Count for: ", i, " is: ", count_limit[i])


def usage_semcor_convertion():
    ss = sc2ss('be%2:42:06::')
    print('here', ss)
    print(ss, ss.definition())
    print(ss.lexname())
    print('(%08d-%s)' % (ss.offset(), ss.pos()))


def usage_wordnet_lemma_and_synsets():
    # LEMMAS
    print(wordnet.lemmas('produce'))
    # SYNSETS
    for synset in wordnet.synsets('book'):
        print("<----------------------------------------------------------->")
        print("Synset name :  ", synset.name())
        # Defining the word
        print("Synset meaning : ", synset.definition())
        print("Lemmas: ", synset.lemmas())
        # list of phrases that use the word in context
        print("Synset example : ", synset.examples())
        print("Synset abstract term :  ", synset.hypernyms())
        for hypernyms in synset.hypernyms():
            print("Synset specific term :  ", hypernyms.hyponyms())
        synset.root_hypernyms()
        print("Synset root hypernerm :  ", synset.root_hypernyms())
        # semcor.chunks()

    ss = sc2ss('be%2:42:06::')
    print('here', ss)
    print(ss, ss.definition())
    print(ss.lexname())
    print('(%08d-%s)' % (ss.offset(), ss.pos()))


if __name__ == "__main__":
    # usage_wordnet_lemma_and_synsets()
    process_semcor()
    create_statistics_from_semcor_and_categories("semcor_frequencies.json")
