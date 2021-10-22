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


def index_words_term_freq_doc_freq_for_category(index, doc_freq_index, text, category):
    tokenized_text = [word.lower() for word in word_tokenize(text) if check(word)]
    doc_freq_index[category] = len(tokenized_text)

    tokenized_text_length = len(tokenized_text)
    if category not in index:
        index[category] = dict()
    for position_word1 in range(0, tokenized_text_length):
        for position_word2 in range(position_word1 + 1, tokenized_text_length):
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
