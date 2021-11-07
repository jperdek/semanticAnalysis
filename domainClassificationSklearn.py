
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.svm import LinearSVC
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import json
import random
import re
import pickle


def separate_with_space(array):
    return ' '.join(array)


def save_as_json(object_to_save, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(object_to_save, file)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def apply_lemmatization_with_pos_tagging(data):
    tag_map = defaultdict(lambda: wordnet.NOUN)
    tag_map['J'] = wordnet.ADJ
    tag_map['V'] = wordnet.VERB
    tag_map['R'] = wordnet.ADV
    lemmatized_data = []
    for sentence in data:
        lemmatized_words = []
        word_lemmatized = WordNetLemmatizer()
        tokenized = word_tokenize(sentence.lower())

        for word, tag in pos_tag(tokenized):
            if word not in stopwords.words('english') and len(word) > 2 and word.isalpha():
                word_final = word_lemmatized.lemmatize(word, tag_map[tag[0]])
                lemmatized_words.append(word_final)
        lemmatized_data.append(separate_with_space(lemmatized_words))
    return lemmatized_data


def classify(train_file, test_file, no_unexpected_values=False):
    training_data_json = load_as_json(train_file)
    random.shuffle(training_data_json)
    test_data_json = load_as_json(test_file)
    random.shuffle(test_data_json)

    training_data = []
    training_labels = []
    category_dict = dict()
    counter_categories = 0
    count_cat_dict = dict()
    for dictionary in training_data_json:
        for key in dictionary.keys():
            if key == 'category':
                category = dictionary[key]
                if category not in count_cat_dict:
                    count_cat_dict[category] = 1
                else:
                    count_cat_dict[category] = count_cat_dict[category] + 1

                if category not in category_dict:
                    category_dict[category] = counter_categories
                    counter_categories = counter_categories + 1
                training_labels.append(category_dict[category])
            elif key == 'text':
                training_data.append(dictionary[key])
            elif not no_unexpected_values:
                print("Error: unexpected key: " + key)

    print(count_cat_dict)
    test_data = []
    test_labels = []
    for dictionary in test_data_json:
        for key in dictionary.keys():
            if key == 'category':
                category = dictionary[key]

                if category not in count_cat_dict:
                    count_cat_dict[category] = 1
                else:
                    count_cat_dict[category] = count_cat_dict[category] + 1

                if category not in category_dict:
                    print("Error: category " + category + "not in categories")
                test_labels.append(category_dict[category])
            elif key == 'text':
                test_data.append(dictionary[key])
            elif not no_unexpected_values:
                print("Error: unexpected key: " + key)

    print(count_cat_dict)
    print(category_dict)
    # trainingLemmatizedData = apply_lemmatization_with_pos_tagging(training_data)
    # testLemmatizedData = apply_lemmatization_with_pos_tagging(test_data)

    training_data = [re.sub(r'[^0-9a-zA-Z ]+', '', str(result).lower()) for result in training_data]
    test_data = [re.sub(r'[^0-9a-zA-Z ]+', '', str(result).lower()) for result in test_data]

    training_data = [str(result).lower() for result in training_data]
    test_data = [str(result).lower() for result in test_data]

    count_vectorizer = CountVectorizer(stop_words="english")
    coun_train = count_vectorizer.fit_transform(training_data)
    count_test = count_vectorizer.transform(test_data)

    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
    tfidf_train = tfidf_vectorizer.fit_transform(training_data)
    tfidf_test = tfidf_vectorizer.transform(test_data)

    with open("tfidf_text_categories.pickle", "wb") as file_to_store:
        pickle.dump(tfidf_vectorizer, file_to_store)

    multinomial_nb_count = MultinomialNB(alpha=0.9)
    multinomial_nb_count.fit(coun_train, training_labels)
    pred_count = multinomial_nb_count.predict(count_test)
    score_count_nb = metrics.accuracy_score(test_labels, pred_count)
    score_count_nbf = metrics.f1_score(test_labels, pred_count, average="micro")
    print("Accuracy score Naive Bayes multinomial count: ", score_count_nb)
    print("F1 score Naive Bayes multinomial count: ", score_count_nbf)

    multinomial_nb_tfidf = MultinomialNB(alpha=0.9)
    multinomial_nb_tfidf.fit(tfidf_train, training_labels)
    pred_tfidf = multinomial_nb_tfidf.predict(tfidf_test)
    score_tfidf_nb = metrics.accuracy_score(test_labels, pred_tfidf)
    score_tfidf_nbf = metrics.f1_score(test_labels, pred_tfidf, average="micro")
    print("Accuracy score Naive Bayes multinomial tfidf: ", score_tfidf_nb)
    print("F1 score Naive Bayes multinomial tfidf: ", score_tfidf_nbf)

    linear_svc_count = LinearSVC()
    linear_svc_count.fit(coun_train, training_labels)
    pred_linear_svc_count = linear_svc_count.predict(count_test)
    score_count_linear_svc = metrics.accuracy_score(test_labels, pred_linear_svc_count)
    score_count_linear_svcf = metrics.f1_score(test_labels, pred_linear_svc_count, average="micro")
    print("Accuracy score Linear SVC multinomial count: ", score_count_linear_svc)
    print("F1 score Linear SVC multinomial count: ", score_count_linear_svcf)

    linear_svc_tfidf = LinearSVC(max_iter=7600)
    linear_svc_tfidf.fit(tfidf_train, training_labels)
    pred_linear_svc_tfidf = linear_svc_tfidf.predict(tfidf_test)
    score_linear_svc_tfidf = metrics.accuracy_score(test_labels, pred_linear_svc_tfidf)
    score_linear_svc_tfidf_f = metrics.f1_score(test_labels, pred_linear_svc_tfidf, average="micro")
    print("Accuracy score LinearSVC multinomial tfidf: ", score_linear_svc_tfidf)
    print("F1 score LinearSVC multinomial tfidf: ", score_linear_svc_tfidf_f)

    with open("linear_svc_text_categories.pickle", "wb") as file_to_store:
        pickle.dump(linear_svc_tfidf, file_to_store)

    passive_aggresive_count = PassiveAggressiveClassifier()
    passive_aggresive_count.fit(coun_train, training_labels)
    pred_passive_aggresive_count = passive_aggresive_count.predict(count_test)
    score_count_passive_aggresive = metrics.accuracy_score(test_labels, pred_passive_aggresive_count)
    score_count_passive_aggresive_f = metrics.f1_score(test_labels, pred_passive_aggresive_count, average="micro")
    print("Accuracy score Passive Aggresive multinomial count: ", score_count_passive_aggresive)
    print("F1 score Passive Aggresive multinomial count: ", score_count_passive_aggresive_f)

    passive_aggresive_tfidf = PassiveAggressiveClassifier()
    passive_aggresive_tfidf.fit(tfidf_train, training_labels)
    pred_passive_aggresive_tfidf = passive_aggresive_tfidf.predict(tfidf_test)
    score_tfidf_passive_aggresive = metrics.accuracy_score(test_labels, pred_passive_aggresive_tfidf)
    score_tfidf_passive_aggresive_f = metrics.f1_score(test_labels, pred_passive_aggresive_tfidf, average="micro")
    print("Accuracy score Passive Aggresive multinomial tfidf: ", score_tfidf_passive_aggresive)
    print("F1 score Passive Aggresive multinomial tfidf: ", score_tfidf_passive_aggresive_f)

    sgd_count = SGDClassifier()
    sgd_count.fit(coun_train, training_labels)
    pred_sgd_count = sgd_count.predict(count_test)
    score_count_sgd = metrics.accuracy_score(test_labels, pred_sgd_count)
    score_count_sgd_f = metrics.f1_score(test_labels, pred_sgd_count, average="micro")
    print("Accuracy score SGD multinomial count: ", score_count_sgd)
    print("F1 score SGD multinomial count: ", score_count_sgd_f)

    sgd_tfidf = PassiveAggressiveClassifier()
    sgd_tfidf.fit(tfidf_train, training_labels)
    pred_sgd_tfidf = sgd_tfidf.predict(tfidf_test)
    score_tfidf_sgd = metrics.accuracy_score(test_labels, pred_sgd_tfidf)
    score_tfidf_sgd_f = metrics.f1_score(test_labels, pred_sgd_tfidf, average="micro")
    print("Accuracy score SGD multinomial tfidf: ", score_tfidf_sgd)
    print("F1 score SGD multinomial tfidf: ", score_tfidf_sgd_f)


def analyse_weir_cetd_files():
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_cetd_extractor.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_cetd_extractor.json",
             no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_cetd__edgare_extractor.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_cetd_edgare_extractor.json",
             no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_cetd_variant_extractor.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_cetd_variant_extractor.json",
             no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_cetd_extractor_whole.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_cetd_extractor_whole.json",
             no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_cetd__edgare_extractor_whole.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_cetd_edgare_extractor_whole.json", no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_cetd_variant_extractor_whole.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_cetd_variant_extractor_whole.json", no_unexpected_values=False)


def analyse_weir_som_files():
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_beautifulsoup.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_beautifulsoup.json",
             no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_beautifulsoup_whole.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_beautifulsoup_whole.json",
             no_unexpected_values=False)


def analyse_swde_som_files():
    classify("output/pageAnalyser/train_beautifulsoup_swde.json", "output/pageAnalyser/test_beautifulsoup_swde.json",
             no_unexpected_values=False)
    classify("output/pageAnalyser/train_beautifulsoup_swde_whole.json",
             "output/pageAnalyser/test_beautifulsoup_swde_whole.json",
             no_unexpected_values=False)


def analyse_weir_plain_files():
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_plain.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_plain.json",
             no_unexpected_values=False)
    classify("serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/train_plain_whole.json",
             "serverParts/apis/http/api/segmentationAnalysis/pageAnalyser/test_plain_whole.json",
             no_unexpected_values=False)


def analyse_weir():
    analyse_weir_cetd_files()
    analyse_weir_som_files()
    analyse_weir_plain_files()


def analyze_text_categories():
    classify("text_categories_train.json",
             "text_categories_test.json",
             no_unexpected_values=True)


if __name__ == "__main__":
    # classify("./pageAnalyser/train_beautifulsoup.json", "./pageAnalyser/test_beautifulsoup.json",
    #         no_unexpected_values=False)
    #analyse_weir()
    #analyse_swde_som_files()
    #analyse_weir()
    analyze_text_categories()
