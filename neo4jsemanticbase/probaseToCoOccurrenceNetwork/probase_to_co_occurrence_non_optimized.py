from typing import Optional

from neo4jsemanticbase.cooccurrence_network.contentFileParsersNeo4j.content_parser \
    import create_token_if_not_exists, get_token_connection
from neo4jsemanticbase.cooccurrence_network.network_creation import CoOccurrenceManager
from serverParts.apis.http.api.textUnderstanding.textPreprocessing import POSTagging


def load_probase_to_network(probase_file_path: str,
                            co_occurrence_network: CoOccurrenceManager,
                            use_pos=True,
                            db_name="neo4j") -> None:
    pos_tagging = None
    if use_pos:
        pos_tagging = POSTagging()
    pos_token1 = None
    pos_token2 = None

    with open(probase_file_path, "r", encoding="utf-8") as file:
        for line in file:
            token1, token2, value = line.split('\t')

            token1 = token1.replace("'", "\\'")
            token2 = token2.replace("'", "\\'")
            if use_pos:
                pos_token1 = pos_tagging.pos_of_word(token1)
                pos_token2 = pos_tagging.pos_of_word(token2)
            co_occurrence_network.process_data_transaction((token1, pos_token1), create_token_if_not_exists, db_name)
            co_occurrence_network.process_data_transaction((token2, pos_token2), create_token_if_not_exists, db_name)
            connection = co_occurrence_network.process_data_transaction(
                (token1, token2, pos_token1, pos_token2), get_token_connection, db_name)
            new_doc = connection.get('_doc')
            if not new_doc:
                new_doc = value
            else:
                print("Doc found - connection exists! " + str(new_doc))
            co_occurrence_network.process_data_transaction((token1, token2, pos_token1, pos_token2, new_doc),
                                                           _update_sum_doc_for_token_connection, db_name)


def _update_sum_doc_for_token_connection(tx,
                                         token1: str, token2: str,
                                         pos_token1: Optional[str],
                                         pos_token2: Optional[str],
                                         doc: int, db_name: str) -> None:
    if not pos_token1 or not pos_token2:
        result = tx.run("""
            USE """ + db_name + """
            MATCH (a:Token {name: '""" + token1 + """'})-[conn:OCCUR]->(b:Token {name: '""" + token2 + """'})
            SET conn += {_doc:""" + str(doc) + """}
            RETURN True
        """)
    else:
        result = tx.run("""
            USE """ + db_name + """
            MATCH (a:Token {name: '""" + token1 + """', pos: '""" + pos_token1[1] + """'})
            -[conn:OCCUR]->(b:Token {name: '""" + token2 + """', pos: '""" + pos_token2[1] + """'})
            SET conn += {_doc:""" + str(doc) + """}
            RETURN True
        """)
    return result


if __name__ == "__main__":
    network = CoOccurrenceManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
    load_probase_to_network('D://dipldatasets/data-concept-instance-relations.txt', network)
    network.close()
