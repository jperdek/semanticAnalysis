import string

try:
    from apis.http.api.graphProcessing.network_manager import get_properties, NetworkManager
    from apis.http.api.textUnderstanding.textPreprocessing import POSTagging
except ImportError:
    from serverParts.apis.http.api.graphProcessing.network_manager import get_properties, NetworkManager
    from serverParts.apis.http.api.textUnderstanding.textPreprocessing import POSTagging


def aggregate_from_given_meaning(tx, typed_word_list: list, db_name: str):
    typed_word_string = ""
    for typed_word in typed_word_list:
        typed_word_string = typed_word_string + ", '" + typed_word + "'"
    typed_word_string = typed_word_string[1:]
    result = tx.run("""
            USE """ + db_name + """
            MATCH (concept)<-[connection:OCCUR]-(typed_word)    
            WHERE typed_word.name IN [ """ + typed_word_string + """ ] 
            RETURN concept, SUM(connection._doc) AS priority,
            apoc.map.mergeList(COLLECT(apoc.map.fromValues([typed_word.name, apoc.convert.toString(connection._doc)])))
            ORDER BY priority DESC
            LIMIT 25""")
    for concept, priority, meanings in result:
        print("Meaning: " + get_properties(concept)["name"] +
              ", priority: " + str(priority) + ", matched: " + str(meanings))
    return result


def get_full_text_results(tx, typed_word_list: list, db_name="neo4j") -> list:
    typed_word_string = ""
    for typed_word in typed_word_list:
        typed_word_string = typed_word_string + "OR " + typed_word + " "
    typed_word_string = typed_word_string[2:]
    # needs call: CALL db.index.fulltext.createNodeIndex("nameLookup",["Token"],["name"])
    result = tx.run("""
                    USE """ + db_name + """
                    CALL db.index.fulltext.queryNodes("nameLookup", '""" + typed_word_string + """') 
                    YIELD node, score
                    RETURN node.name, score 
                    ORDER BY score DESC
                    LIMIT 25""")
    return result


def aggregate_from_given_meaning_full_text(tx, typed_word_list: list, db_name: str, mix: bool = False):
    typed_word_string = ""
    for name, score in get_full_text_results(tx, typed_word_list):
        typed_word_string = typed_word_string + ", '" + name.strip().replace("'", "\\'") + "'"
    if mix:
        for typed_word in typed_word_list:
            typed_word_string = typed_word_string + ", '" + typed_word + "'"
    typed_word_string = typed_word_string[1:]

    result = tx.run("""
            USE """ + db_name + """
            MATCH (concept)<-[connection:OCCUR]-(typed_word)    
            WHERE typed_word.name IN [ """ + typed_word_string + """ ] 
            RETURN concept, SUM(connection._doc) AS priority,
            apoc.map.mergeList(COLLECT(apoc.map.fromValues([typed_word.name, apoc.convert.toString(connection._doc)])))
            ORDER BY priority DESC
            LIMIT 25""")
    for concept, priority, meanings in result:
        print("Meaning: " + get_properties(concept)["name"] +
              ", priority: " + str(priority) + ", matched: " + str(meanings))
    return result


def aggregate_meanings_from_concept(tx, concept_word_list: list, db_name: str):
    concept_word_string = ""
    for concept_word in concept_word_list:
        concept_word_string = concept_word_string + ", '" + concept_word + "'"
    concept_word_string = concept_word_string[1:]
    result = tx.run("""
                USE """ + db_name + """
                MATCH (concept)<-[connection:OCCUR]-(typed_word)    
                WHERE concept.name IN [ """ + concept_word_string + """ ] 
                RETURN typed_word, SUM(connection._doc) AS priority,
                apoc.map.mergeList(COLLECT(apoc.map.fromValues([concept.name, apoc.convert.toString(connection._doc)])))
                ORDER BY priority DESC
                LIMIT 25""")
    for concept, priority, meanings in result:
        print("Meaning: " + get_properties(concept)["name"] +
              ", priority: " + str(priority) + ", matched: " + str(meanings))
    return result


def aggregate_meanings_from_concept_full_text(tx, concept_word_list: list, db_name: str):
    concept_word_string = ""
    for name, score in get_full_text_results(tx, concept_word_list):
        concept_word_string = concept_word_string + ", '" + name.strip().replace("'", "\\'") + "'"
    concept_word_string = concept_word_string[1:]

    result = tx.run("""
                USE """ + db_name + """
                MATCH (concept)<-[connection:OCCUR]-(typed_word)    
                WHERE concept.name IN [ """ + concept_word_string + """ ] 
                RETURN typed_word, SUM(connection._doc) AS priority,
                apoc.map.mergeList(COLLECT(apoc.map.fromValues([concept.name, apoc.convert.toString(connection._doc)])))
                ORDER BY priority DESC
                LIMIT 25""")
    for concept, priority, meanings in result:
        print("Meaning: " + get_properties(concept)["name"] +
              ", priority: " + str(priority) + ", matched: " + str(meanings))
    return result


def preprocess_text(text: str):
    pos_tagger = POSTagging()
    list_of_words = [word.strip(string.punctuation) for word in text.split() if word.strip(
            string.punctuation) != '' and len(word) > 3]
    concept_candidate_list = []
    for word, pos_tag in pos_tagger.lemmatization_and_stop_words_removal_batch_pairs(list_of_words, 'english'):
        if pos_tag == 'n':
            concept_candidate_list.append(word.lower())
    return concept_candidate_list


if __name__ == "__main__":
    database_name = "neo4j"
    network = NetworkManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
    network.initialize_additional_indexes()
    text_for_analysis = """To Americans of the 1920s and ‘30s, he was the notorious gangster Scarface Al, Public Enemy 
                       No. 1. But when he arrived at Alcatraz in late August of 1934, Alphonse “Al” Capone took on a 
                       more humbling name: Prisoner 85. 
                       As Prisoner 85, Al Capone led a very different life from his freewheeling days at the top of the 
                       Chicago rackets. He became a serious reader, a musician and a composer. A model prisoner, 
                       he kept a low profile, did his prison chores and rarely resorted to violence unless he was 
                       provoked—in one instance bashing a fellow inmate’s head with a bedpan.
                       It would be a stretch to say that Al Capone was the Renaissance man of Alcatraz, but he appears
                       """
    concepts = preprocess_text(text_for_analysis)
    # not as much good results - getting meaning from concepts are less accurate if there are not enough meaning matches
    # domains
    # = network.process_data_transaction(tuple([concepts]), aggregate_meanings_from_concept, database_name)
    similar_meanings = network.process_data_transaction(tuple([concepts]), aggregate_from_given_meaning, database_name)
    # similar_meanings
    # = network.process_data_transaction(tuple([concepts]), aggregate_from_given_meaning_full_text, database_name)
    similar_meanings1 =\
        network.process_data_transaction(tuple([concepts]), aggregate_from_given_meaning_full_text, database_name)
    # similar_meanings
    # = network.process_data_transaction(tuple([concepts]), aggregate_meanings_from_concept_full_text, database_name)
    network.close()
