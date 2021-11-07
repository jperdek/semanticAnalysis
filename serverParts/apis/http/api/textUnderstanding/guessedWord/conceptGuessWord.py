import math
import json


def count_changed_tfid(x_in_case_y: float, x_in_case_z: float, n: int, neighbour_n: int):
    if neighbour_n == 0.0 or x_in_case_z == 0.0:
        return 0.0
    return (x_in_case_y / x_in_case_z) * math.log(n / neighbour_n)


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def count_tf_idf(text: str, index: dict, category: str, window: int = 20):
    n = index[category]["_count"]
    maximum = 0
    focus = 0

    text_words = text.split()
    tokenized_text_length = len(text_words)
    for position_word1 in range(0, tokenized_text_length):
        word1 = text_words[position_word1]

        window_range = position_word1 + 1 + window
        if window_range > tokenized_text_length:
            window_range = tokenized_text_length

        if word1 in index[category]:
            result_sum = 0
            for position_word2 in range(position_word1 + 1, window_range):
                word2 = text_words[position_word2]
                if word2 in index[category][word1]:
                    if word2 in index[category]:
                        count_neighbour = index[category][word2]["_count"]
                    else:
                        count_neighbour = 1

                    result_sum = result_sum + count_changed_tfid(index[category][word1][word2]["sum"],
                                             index[category][word1][word2]["_other"], n, count_neighbour)
            if maximum < result_sum:
                maximum = result_sum
                focus = position_word1
    return maximum


def get_texts_from_range(text: str, index: dict, category: str,
                         tf_idf_maximum: float, tf_idf_range: float = 2.0, window: int = 20):
    n = index[category]["_count"]
    maximum = 0
    results = []

    text_words = text.split()
    tokenized_text_length = len(text_words)
    for position_word1 in range(0, tokenized_text_length):
        word1 = text_words[position_word1]

        window_range = position_word1 + 1 + window
        if window_range > tokenized_text_length:
            window_range = tokenized_text_length

        if word1 in index[category]:
            result_sum = 0
            for position_word2 in range(position_word1 + 1, window_range):
                word2 = text_words[position_word2]
                if word2 in index[category][word1]:
                    if word2 in index[category]:
                        count_neighbour = index[category][word2]["_count"]
                    else:
                        count_neighbour = 1
                    result_sum = result_sum + count_changed_tfid(index[category][word1][word2]["sum"],
                                             index[category][word1][word2]["_other"], n, count_neighbour)
            if maximum >= tf_idf_maximum - tf_idf_range:
                result = []
                for focus in range(position_word1, position_word1 + window):
                    if focus >= tokenized_text_length:
                        break
                    result.append(text_words[focus])
                results.append(result)
    return results


if __name__ == '__main__':
    index_json = load_as_json("../../../../../../output/index-cat-all.json")
    sample_text = 'To Americans of the 1920s and ‘30s, he was the notorious gangster Scarface Al, Public Enemy No. 1. But when he arrived at Alcatraz in late August of 1934, Alphonse “Al” Capone took on a more humbling name: Prisoner 85. '\
                  'As Prisoner 85, Al Capone led a very different life from his freewheeling days at the top of the Chicago rackets. He became a serious reader, a musician and a composer. A model prisoner, he kept a low profile, did his prison chores and rarely resorted to violence unless he was provoked—in one instance bashing a fellow inmate’s head with a bedpan.'\
                  'It would be a stretch to say that Al Capone was the Renaissance man of Alcatraz, but he appears to have lived up to his promise to mend his evil ways—at least temporarily.'
    category = "historical"

    maximum = count_tf_idf(sample_text, index_json, category)
    results = get_texts_from_range(sample_text, index_json, category, maximum)
    for index, result in enumerate(results):
        print(index)
        print(" ".join(result))
