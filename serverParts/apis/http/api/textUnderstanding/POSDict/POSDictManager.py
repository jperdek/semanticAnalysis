import json


class POSDict:

    @staticmethod
    def load_json(file_name: str):
        with open(file_name, encoding='utf-8') as file_path:
            return json.load(file_path)

    def __init__(self, pos_dict_path: str):
        self.pos_dict = POSDict.load_json(pos_dict_path)

    def search_wod_senses(self, word: str):
        word_upper = word.upper()
        if len(self.pos_dict[word_upper]['MEANINGS']) == 0:
            for synonym in self.pos_dict[word_upper]['SYNONYMS']:
                if len(self.pos_dict[synonym.upper()]) > 0:
                    pass