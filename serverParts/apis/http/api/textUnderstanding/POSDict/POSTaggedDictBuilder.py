import json
import os


class POSDictBuilder:

    @staticmethod
    def merge_two_dicts(dict1: dict, dict2: dict):
        dict1.update(dict2)
        return dict1

    @staticmethod
    def load_json(file_name: str):
        with open(file_name, encoding='utf-8') as file_path:
            return json.load(file_path)

    @staticmethod
    def save_as_json(data: dict, file_name: str):
        with open(file_name, "w", encoding='utf-8') as f:
            f.write(json.dumps(data))

    @staticmethod
    def get_meanings(target_meaning: dict) -> list:
        meanings = list()
        for value in target_meaning.values():
            meaning = dict()
            other_values = value
            meaning['pos'] = other_values[0]
            meaning['description'] = list()
            meaning['description'].append(other_values[1])
            for other_meanings in other_values[2:]:
                if type(other_meanings) == list:
                    for other_meanings2 in other_meanings:
                        meaning['description'].append(other_meanings2)
                else:
                    print('Error: not list: ' + str(other_meanings))

            meanings.append(meaning)
        return meanings

    @staticmethod
    def build_dict(path_to_dict_folder: str):
        merged_dict = dict()
        for json_dict_file in os.listdir(path_to_dict_folder):
            path_to_dict_part = os.path.join(path_to_dict_folder, json_dict_file)
            resulting_parts = POSDictBuilder.load_json(path_to_dict_part)
            for word_name, attributes in resulting_parts.items():
                merged_dict[word_name] = dict()
                for key, value in attributes.items():
                    if key == 'MEANINGS':
                        result_meaning = POSDictBuilder.get_meanings(value)
                        if len(result_meaning) > 0:
                            merged_dict[word_name]['MEANINGS'] = result_meaning
                    elif key == 'ANTONYMS':
                        if len(value) > 0:
                            merged_dict[word_name]['ANTONYMS'] = value
                    elif key == 'SYNONYMS':
                        if len(value) > 0:
                            merged_dict[word_name]['SYNONYMS'] = value
                    else:
                        print("Error: unknown dict part: " + key)
        return merged_dict


if __name__ == "__main__":
    post_dist_builder = POSDictBuilder()
    merged_dict_final = post_dist_builder.build_dict('D://dipldatasets/pos_tagged_dict/')
    POSDictBuilder.save_as_json(merged_dict_final, 'post_tagged_dict.json')
