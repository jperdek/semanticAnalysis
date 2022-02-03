import neo4j
from nltk.tokenize import word_tokenize
import math
from neo4jsemanticbase.cooccurrence_network.network_creation import CoOccurrenceManager, set_properties


def check(word: str) -> bool:
    return len(word) > 3 and word.isalpha()


def parse_text(text, co_occurrence_network: CoOccurrenceManager, window: int = 20, db_name="neo4j") -> None:
    tokenized_text = [word.lower() for word in word_tokenize(text) if check(word)]

    tokenized_text_length = len(tokenized_text)
    for position_word1 in range(0, tokenized_text_length):
        window_range = position_word1 + 1 + window
        if window_range > tokenized_text_length:
            window_range = tokenized_text_length

        for position_word2 in range(position_word1 + 1, window_range):
            word1 = str(tokenized_text[position_word1])
            word2 = str(tokenized_text[position_word2])
            co_occurrence_network.process_data_transaction(tuple([word1]), _create_token_if_not_exists, db_name)
            co_occurrence_network.process_data_transaction(tuple([word2]), _create_token_if_not_exists, db_name)
            connection = co_occurrence_network.process_data_transaction((word1, word2), _get_token_connection, db_name)
            previous_sum = connection.get('_sum')
            previous_doc = connection.get('_doc')
            if not previous_sum:
                previous_sum = 0.0
            if not previous_doc:
                previous_doc = 0
 
            new_doc = previous_doc + 1
            new_sum = previous_sum + math.pow(math.e, -(position_word2 - position_word1 - 1.0))
            co_occurrence_network.process_data_transaction((word1, word2, new_doc, new_sum),
                                                           _update_sum_doc_for_token_connection, db_name)


def _create_token_if_not_exists(tx, token: str, db_name: str) -> None:
    tx.run("""
        USE """ + db_name + """
        MERGE (a:Token {name: '""" + token + """'})
    """)


def _get_token_connection(tx, token1: str, token2: str, db_name: str) -> neo4j.Record:
    result = tx.run("""
        USE """ + db_name + """
        MATCH (a:Token {name: '""" + token1 + """'}), (b:Token {name: '""" + token2 + """'})
        MERGE (a)-[conn:OCCUR]->(b)
        RETURN conn
    """)
    connection_result = result.single()[0]
    if connection_result:
        return set_properties(connection_result)
    return connection_result


def _update_sum_doc_for_token_connection(tx, token1: str, token2: str, doc: int, sum: float, db_name: str) -> None:
    result = tx.run("""
            USE """ + db_name + """
            MATCH (a:Token {name: '""" + token1 + """'})-[conn:OCCUR]->(b:Token {name: '""" + token2 + """'})
            SET conn += {_doc:""" + str(doc) + """, _sum:""" + str(sum) + """}
            RETURN True
        """)
    return result


if __name__ == "__main__":
    try:
        network = CoOccurrenceManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
        parse_text("""To Americans of the 1920s and ‘30s, he was the notorious gangster Scarface Al, Public Enemy 
                   No. 1. But when he arrived at Alcatraz in late August of 1934, Alphonse “Al” Capone took on a 
                   more humbling name: Prisoner 85. 
                   To Americans of the 1920s and ‘30s, he was the notorious gangster Scarface Al, Public Enemy 
                   No. 1. But when he arrived at Alcatraz in late August of 1934, Alphonse “Al” Capone took on a 
                   more humbling name: Prisoner 85. 
                   As Prisoner 85, Al Capone led a very different life from his freewheeling days at the top of the 
                   Chicago rackets. He became a serious reader, a musician and a composer. A model prisoner, 
                   he kept a low profile, did his prison chores and rarely resorted to violence unless he was 
                   provoked—in one instance bashing a fellow inmate’s head with a bedpan.
                   It would be a stretch to say that Al Capone was the Renaissance man of Alcatraz, but he appears 
                   to have lived up to his promise to mend his evil ways—at least temporarily.""",
                   network, window=20, db_name="neo4j")
        network.close()
    except Exception as e:
        with open("error.txt", "w", encoding="utf-8") as file:
            file.write(str(e))
            raise e
