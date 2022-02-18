from neo4jsemanticbase.cooccurrence_network.network_creation import CoOccurrenceManager


def get_associated_information_according_wordnet_domains(co_occurrence_network: CoOccurrenceManager, db_name="neo4j"):
    domains = co_occurrence_network.process_data_transaction_without_arguments(_get_all_wordnet_domains, db_name)
    for domain in domains:
        print(domain)
        # re = co_occurrence_network.process_data_transaction(
        #    tuple([str(domain)]), _get_associated_data_to_wornet_domain, db_name)
        res = co_occurrence_network.process_data_transaction(
            tuple([str(domain)]), _get_associated_data_connection_to_wornet_domain, db_name)
        break


def _get_all_wordnet_domains(tx, db_name: str) -> list:
    result = tx.run("""
            USE """ + db_name + """ 
            MATCH ()-[r:ns0__hasWordnetDomain]->(wordnet_domain)
            RETURN wordnet_domain, ID(wordnet_domain) LIMIT 25""")
    node_list = []
    for node, id_node in result:
        node_list.append(id_node)

    return node_list


def get_properties(self):
    if hasattr(self, '_properties'):
        return self._properties
    return None


def _get_associated_data_to_wornet_domain(tx, wordnet_domain_id: str, db_name: str) -> list:
    result = tx.run("""
        USE """ + db_name + """
        MATCH (wordnet_domain)<-[]-(follower)
        WHERE ID(wordnet_domain) = """ + wordnet_domain_id + """ 
        RETURN follower""")
    data_list = []
    for node in result:
        for node_data_name, node_data_value in node.data()["follower"].items():
            if "label" in node_data_name.lower():  # or "glos" in node_data_name.lower():
                if node_data_value not in data_list:
                    data_list.append(node_data_value)
    print(data_list)
    return data_list


def _get_associated_data_connection_to_wornet_domain(tx, wordnet_domain_id: str, db_name: str) -> list:
    result = tx.run("""
        USE """ + db_name + """
        MATCH (wordnet_domain)<-[connection]-(follower)
        WHERE ID(wordnet_domain) = """ + wordnet_domain_id + """ 
        RETURN connection, follower""")
    data_list = []
    for connection, node in result:
        print(connection.type)
        print(node)
        for node_data_name, node_data_value in get_properties(node).items():
            if "label" in node_data_name.lower():  # or "glos" in node_data_name.lower():
                if node_data_value not in data_list:
                    data_list.append(node_data_value)
    print(data_list)
    return data_list


def _match_data_associated_with_domain(tx, domain_name: str, db_name: str) -> None:
    tx.run("""
        USE """ + db_name + """ 
        MATCH (n: { name: '')-[]-(m)
        RETURN n,m""")


if __name__ == "__main__":
    network = CoOccurrenceManager("bolt://localhost:7687", "neo4j", "perdekj", "neo4j")
    get_associated_information_according_wordnet_domains(network)
    network.close()