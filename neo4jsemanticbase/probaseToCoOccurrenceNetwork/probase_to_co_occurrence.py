import json
from typing import Union
from neo4jsemanticbase.cooccurrence_network.network_creation import CoOccurrenceManager
from serverParts.apis.http.api.textUnderstanding.textPreprocessing import POSTagging


def load_probase_to_network(optimized_probase_file_path: str,
                            co_occurrence_network: CoOccurrenceManager,
                            update_frequency=1000,
                            db_name="neo4j") -> None:
    with open(optimized_probase_file_path, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            connections = ""
            concept_name, raw_concept_data = line.split('\t')
            concept_data = json.loads(raw_concept_data)
            concept_name = concept_name.replace("'", "\\'")
            matches = start_matches = "(t:Token { name: '" + concept_name + "'}),"

            for typed_word_index, (typed_word_name, value) in enumerate(concept_data.items()):
                if typed_word_index % update_frequency == 0 and typed_word_index != 0:
                    print("update")
                    matches = matches[:-1]
                    connections = connections[:-1]
                    co_occurrence_network.process_data_transaction((matches, connections), _create_with_match_data,
                                                                   db_name)
                    matches = start_matches
                    connections = ""
                typed_word_name = typed_word_name.replace("'", "\\'")
                matches = matches + "(a" + str(typed_word_index) + ":Token { name:'" + typed_word_name + "'}),"
                connections = \
                    "(t)-[:OCCUR {_doc:" + str(value) + "}]->(a" + str(typed_word_index) + ")," + connections
            if connections != "":
                matches = matches[:-1]
                connections = connections[:-1]
                co_occurrence_network.process_data_transaction((matches, connections), _create_with_match_data, db_name)
                if index % 10 == 0:
                    print("Inserted: " + str(index))


def load_as_json(filename: str) -> Union[dict, list]:
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def _create_with_match_data(tx, match_data: str, create_data: str, db_name: str) -> None:
    tx.run("""
        USE """ + db_name + """ 
        MATCH """ + match_data + """ 
        CREATE """ + create_data)
    
    
def _create_data(tx, create_data: str, db_name: str) -> None:
    tx.run("""
        USE """ + db_name + """
        CREATE """ + create_data)


def load_probase_entities(unique_names_file: str,
                          co_occurrence_network: CoOccurrenceManager,
                          update_frequency=1000,
                          apply_pos: bool = True,
                          db_name="neo4j") -> None:
    entities = load_as_json(unique_names_file)
    entity_string = ""
    remaining = 0
    if not apply_pos:
        for index, entity_token in enumerate(entities):
            entity_token = entity_token.replace("'", "\\'")
            if index % update_frequency == 0 and index != 0:
                entity_string = entity_string[:-1]
                co_occurrence_network.process_data_transaction(tuple([entity_string]), _create_data, db_name)
                entity_string = ""
                if index % 10000 == 0:
                    print("Inserted instances: " + str(index))
            entity_string = "(:Token {name: '" + entity_token + "'})," + entity_string
            remaining = index
    else:
        pos_tagging = POSTagging()
        for index, entity_token in enumerate(entities):
            entity_token = entity_token.replace("'", "\\'")
            if index % update_frequency == 0 and index != 0:
                entity_string = entity_string[:-1]
                co_occurrence_network.process_data_transaction(tuple([entity_string]), _create_data, db_name)
                entity_string = ""
                if index % 10000 == 0:
                    print("Inserted instances: " + str(index))
            pos_token = pos_tagging.pos_of_word(entity_token)
            entity_string = "(:Token {name: '" + entity_token + "',pos: '" + pos_token[1] + "'})," + entity_string
            remaining = index
    if entity_string != "":
        entity_string = entity_string[:-1]
        co_occurrence_network.process_data_transaction(tuple([entity_string]), _create_data, db_name)
        print("Inserted instances: " + str(remaining))


if __name__ == "__main__":
    network = CoOccurrenceManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
    #load_probase_entities("D://dipldatasets/probase_entities.json", network)
    # MATCHING TAKES REALLY LONG...
    load_probase_to_network("D://dipldatasets/optimized_probase.txt", network)
    network.close()
