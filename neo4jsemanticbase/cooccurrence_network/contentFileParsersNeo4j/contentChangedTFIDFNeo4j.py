import json
from neo4jsemanticbase.cooccurrence_network.network_creation import CoOccurrenceManager
import yaml


def load_as_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def load_text_categories_to_json(co_occurrence_network: CoOccurrenceManager, db_name="neo4j"):
    category_json = load_as_json("../../../output/index-cat-all.json")
    for category_name, category_data in category_json.items():
        print(category_name)
        co_occurrence_network.process_data_transaction(tuple([category_name]), _create_token_if_not_exists, db_name)
        for concept_name, concept_data in category_data.items():
            if concept_name == "_count":
                count_category_name = category_name + "_count"
                co_occurrence_network.process_data_transaction(
                    (category_name, count_category_name, concept_data), _insert_attribute, db_name)
                continue
            co_occurrence_network.process_data_transaction(tuple([concept_name]), _create_token_if_not_exists, db_name)
            co_occurrence_network.process_data_transaction(
                (category_name, concept_name),
                _insert_relation_if_not_exists_without_data, db_name)
            for typed_word_name, typed_word_data in concept_data.items():
                if typed_word_name == "_count":
                    count_concept_name = concept_name + "_count"
                    co_occurrence_network.process_data_transaction(
                        (concept_name, count_concept_name, typed_word_data), _insert_attribute, db_name)
                    continue
                co_occurrence_network.process_data_transaction(tuple([typed_word_name]), _create_token_if_not_exists, db_name)
                co_occurrence_network.process_data_transaction((concept_name, typed_word_name, typed_word_data),
                                                               _insert_relation_if_not_exists, db_name)


def _insert_relation_if_not_exists(tx, token1: str, token2: str, data_content: dict, db_name: str):
    result = tx.run("""
        USE """ + db_name + """
        MATCH (a:Token {name: '""" + token1 + """'}), (b: Token {name: '""" + token2 + """'})
        MERGE (a)-[:OCCUR {""" + yaml.dump(data_content).replace("\n", ",")[:-1] + """}]->(b)
        RETURN True
    """)
    return result


def _insert_relation_if_not_exists_without_data(tx, token1: str, token2: str, db_name: str):
    result = tx.run("""
        USE """ + db_name + """
        MATCH (a:Token {name: '""" + token1 + """'}), (b: Token {name:'""" + token2 + """'})
        MERGE (a)-[:OCCUR]->(b)
        RETURN True
    """)
    return result


def _insert_attribute(tx, token1: str, attribute_name: str, attribute_value: any, db_name: str):
    result = tx.run("""
        USE """ + db_name + """
        MATCH (a:Token {name: '""" + token1 + """'})
        SET a.""" + attribute_name + """=""" + str(attribute_value) + """
        RETURN True
    """)
    return result


def _create_token_if_not_exists(tx, token: str, db_name: str):
    result = tx.run("""
            USE """ + db_name + """
            MERGE (a:Token {name: '""" + token + """'})
            RETURN True
        """)
    return result


if __name__ == "__main__":
    try:
        network = CoOccurrenceManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
        load_text_categories_to_json(network)
        network.close()
    except Exception as e:
        with open("error.txt", "w", encoding="utf-8") as file:
            file.write(str(e))
            raise e
