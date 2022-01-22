try:
    from textUnderstanding.conceptDataNormalization.conceptVectorNormalizationTools import \
        ConceptVectorNormalizationTools
    from textUnderstanding.textPreprocessing import POSTagging
except ImportError:
    from serverParts.apis.http.api.textUnderstanding.conceptDataNormalization.conceptVectorNormalizationTools import \
        ConceptVectorNormalizationTools
    from serverParts.apis.http.api.textUnderstanding.textPreprocessing import POSTagging


def load_values(file_name: str, result_dict: dict):
    number_lines = 0
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            number_lines = number_lines + 1

            text1, text2, value = line.split('\t')
            if len(text1.split()) > 1 or len(text2.split()) > 1:
                continue

            # uncomment for testing purposes - set number clusters to 100 for example
            if len(result_dict) > 1000:
                result_dict[text2][text1] = float(value)
                break

            if text2 not in result_dict:
                result_dict[text2] = dict()
            if number_lines % 1000000 == 0:
                print(1000000)

            result_dict[text2][text1] = float(value)
    print("Whole length: " + str(len(result_dict)))


def normalize_pos_and_lemma_for_data_concept_instance_relations(result_dict: dict,
                                                                file_name: str,
                                                                separator='\t',
                                                                decimal_places=5):
    pos_tagging = POSTagging()
    with open(file_name, "w", encoding="utf-8") as file:
        for context_key, context in result_dict.items():
            vector_position_values = ""
            vector_size = ConceptVectorNormalizationTools.evaluate_vector_size(context.values())
            for vector_position_name, vector_position_value in context.items():
                vector_position_values = vector_position_values + separator \
                                         + vector_position_name + "(" + \
                                         str(round(float(vector_position_value)
                                                   / vector_size, decimal_places)) + ")"
            add_length = separator + str(len(context.keys()))
            # separator between them should be included in second variable
            lemma_concept_key, tag = pos_tagging.lemma_and_pos_of_word(context_key)
            print(lemma_concept_key + " " + tag)
            file.write(lemma_concept_key + "__" + tag + vector_position_values + add_length + "\n")


if __name__ == '__main__':
    main_result_dict = dict()
    load_values('D://dipldatasets/data-concept-instance-relations.txt', main_result_dict)
    normalize_pos_and_lemma_for_data_concept_instance_relations(main_result_dict, "pos_lemma_data.txt")
