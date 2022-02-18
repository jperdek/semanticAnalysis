
from textPreprocessing import POSTagging
import json
import string


def load_json(file):
    with open(file, encoding='utf-8') as file_path:
        return json.load(file_path)


if __name__ == "__main__":
    pos_tagger = POSTagging()
    for record in load_json('D://dipldatasets/datasety/CETD/extractor.json'):
        list_of_words = [word.strip(string.punctuation) for word in record['text'].split() if word.strip(
            string.punctuation) != '']
        print(list_of_words)
        pos_tagger.lemmatization_and_stop_words_removal(list_of_words, 'english')