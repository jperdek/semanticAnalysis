from serverParts.apis.http.api.textUnderstanding.conceptVectorNormalizationTools import ConceptVectorNormalizationTools


def load_values(file_name: str, result_dict: dict):
    number_lines = 0
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            number_lines = number_lines + 1

            text1, text2, value = line.split('\t')
            if len(text1.split()) > 1 or len(text2.split()) > 1:
                continue

            if text2 not in result_dict:
                result_dict[text2] = dict()
            if number_lines % 1000000 == 0:
                print(1000000)

            result_dict[text2][text1] = value
    print("Whole length: " + str(len(result_dict)))


def save_values_for_kmedoid(result_dict: dict, file_name: str, separator='\t'):
    with open(file_name, "w", encoding="utf-8") as file:
        for context_key, context in result_dict.items():
            vector_position_values = ""
            for vector_position_name, vector_position_value in context.items():
                vector_position_values = vector_position_values + separator \
                                         + vector_position_name + "(" +\
                                         str(vector_position_value.replace('\n', '')) + ")"
            add_length = separator + str(len(context.keys()))
            # separator between them should be included in second variable
            file.write(context_key + vector_position_values + add_length + "\n")


if __name__ == "__main__":
    main_result_dict = dict()
    load_values('D://dipldatasets/data-concept-instance-relations.txt', main_result_dict)
    save_values_for_kmedoid(main_result_dict, 'D://dipldatasets/data-concept-instance-relations-remake.txt')

    # normalize values
    ConceptVectorNormalizationTools.save_values_for_kmedoid_concept_normalized(
        main_result_dict, 'D://dipldatasets/data-concept-instance-relations-remake-normalized.txt')
    ConceptVectorNormalizationTools.save_values_for_kmedoid_concept_normalized_as_dict(
        main_result_dict, 'D://dipldatasets/data-concept-instance-relations-remake-normalized.txt')