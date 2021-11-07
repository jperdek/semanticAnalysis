from nltk.tokenize import word_tokenize
import math


def check(word: str) -> bool:
    return len(word) > 3 and word.isalpha()


def index_words_term_freq_doc_freq(index, doc_freq_index, text, category):
    tokenized_text = [word.lower() for word in word_tokenize(text) if check(word)]
    doc_freq_index[category] = len(tokenized_text)

    tokenized_text_length = len(tokenized_text)
    for position_word1 in range(0, tokenized_text_length):
        for position_word2 in range(position_word1 + 1, tokenized_text_length):
            word1 = str(tokenized_text[position_word1])
            word2 = str(tokenized_text[position_word2])
            if word1 not in index:
                index[word1] = dict()
            if word2 in index[word1]:
                if category not in index[word1][word2]['doc']:
                    index[word1][word2]['doc'][category] = 1
                    index[word1][word2]['cf'] = len(index[word1][word2]['doc'])
                else:
                    index[word1][word2]['doc'][category] = index[word1][word2]['doc'][category] + 1
            else:
                index[word1][word2] = {}
                index[word1][word2]['doc'] = {}
                index[word1][word2]['cf'] = 1   # category frequency
                index[word1][word2]['doc'][category] = 1


def index_words_term_freq_doc_freq_tfidf(index, doc_freq_index, text, document_identifier):
    tokenized_text = [word.lower() for word in word_tokenize(text) if check(word)]
    doc_freq_index[document_identifier] = len(tokenized_text)
    #index["_docs"] = index["_docs"] + 0

    for word in tokenized_text:
        word = str(word)
        if word in index:
            if document_identifier not in index[word]['doc']:
                index[word]['doc'][document_identifier] = 1
                index[word]['df'] = len(index[word]['doc'])
            else:
                index[word]['doc'][document_identifier] = index[word]['doc'][document_identifier] + 1
        else:
            index[word] = {}
            index[word]['doc'] = {}
            index[word]['df'] = 1
            index[word]['doc'][document_identifier] = 1


def index_words_term_freq_doc_freq_for_category(index, text, category, window: int = 20):
    tokenized_text = [word.lower() for word in word_tokenize(text) if check(word)]

    tokenized_text_length = len(tokenized_text)
    if category not in index:
        index[category] = dict()
    for position_word1 in range(0, tokenized_text_length):
        window_range = position_word1 + 1 + window
        if window_range > tokenized_text_length:
            window_range = tokenized_text_length

        for position_word2 in range(position_word1 + 1, window_range):
            word1 = str(tokenized_text[position_word1])
            word2 = str(tokenized_text[position_word2])
            if word1 not in index[category]:
                index[category][word1] = dict()
            if word2 in index[category][word1]:
                index[category][word1][word2]['doc'] = index[category][word1][word2]['doc'] + 1
            else:
                index[category][word1][word2] = dict()
                index[category][word1][word2]['doc'] = 1
                index[category][word1][word2]['sum'] = 0.0
            index[category][word1][word2]['sum'] = index[category][word1][word2]['sum'] \
                                                   + math.pow(math.e, -(position_word2 - position_word1 - 1.0))


def remove_index_words_term_freq_doc_freq_for_category(index_category: dict, treshold: int = 5):
    remove_first_words = []
    for word1 in index_category.keys():
        if word1 != "_count":
            remove = list()
            for word2 in index_category[word1].keys():
                if word2 != "_count" and index_category[word1][word2]["doc"] < treshold:
                    remove.append(word2)
            for word2 in remove:
                del index_category[word1][word2]
            if len(index_category[word1]) == 0:
                remove_first_words.append(word1)
    for word1 in remove_first_words:
        del index_category[word1]


def count_changed_tfidf_info(index_category: dict):
    unique_words = dict()
    for word1 in index_category.keys():
        if word1 != "_count":
            for word2 in index_category[word1].keys():
                unique_words[word2] = word2
            index_category[word1]["_count"] = len(index_category[word1])
    index_category["_count"] = len(unique_words)

    for word1 in index_category.keys():
        if word1 != "_count":
            for word2_a in index_category[word1].keys():
                if word2_a != "_count":
                    count = 0
                    for word2_b in index_category[word1].keys():
                        if word2_a != word2_b and word2_b != "_count":
                            count = count + index_category[word1][word2_b]["doc"]
                    index_category[word1][word2_a]["_other"] = count


def count_changed_tfid(x_in_case_y: float, x_in_case_z: float, n: int, neighbour_n: int):
    return (x_in_case_y / x_in_case_z) * math.log(n, neighbour_n)


def count_tf_idf(text: str, index: dict):
    for category in index.keys():
        n = index[category]["_count"]
        text_words = text.split()
        tokenized_text_length = len(text_words)
        for position_word1 in range(0, tokenized_text_length):
            word1 = text_words[position_word1]
            if word1 in index[category]:
                for position_word2 in range(position_word1 + 1, tokenized_text_length):
                    word2 = text_words[position_word2]
                    if word2 in index[category][word1]:
                        if word2 in index[category]:
                            count_neighbour = index[category][word2]["_count"]
                        else:
                            count_neighbour = 1
                        res = count_changed_tfid(index[category][word1][word2]["sum"],
                                                 index[category][word1][word2]["_other"], n, count_neighbour)
                        print(res)