import types

import neo4j


class CoOccurrenceManager:

    def __init__(self, uri, user, password, database_name='CoOccurence'):
        self.driver = neo4j.GraphDatabase.driver(uri, auth=(user, password))
        self.database_name = database_name

    def close(self):
        self.driver.close()

    def create_db_for_network(self, db_name=None):
        if not db_name:
            db_name = self.database_name
        with self.driver.session() as session:
            creation = session.write_transaction(self._create_db, db_name)
            print(creation)

    def process_data_transaction(self, data: tuple, used_function: any, db_name=None):
        if not db_name:
            db_name = self.database_name
        with self.driver.session() as session:
            creation = session.write_transaction(used_function, *data, db_name)
        return creation

    def process_data_transactions(self, data: list, used_function: any, db_name=None):
        if not db_name:
            db_name = self.database_name
        with self.driver.session() as session:
            for data_part in data:
                creation = session.write_transaction(used_function, *data_part, db_name)
        return creation

    @staticmethod
    def _create_db(tx, db_name: str):
        result = tx.run("CREATE DATABASE {name} IF NOT EXISTS".format(name=db_name))
        return result.single()[0]

    def get_data(self, db_name=None):
        if not db_name:
            db_name = self.database_name
        with self.driver.session() as session:
            relations = session.write_transaction(self._list_relations, db_name)
            for relation in relations:
                print(relation)

    @staticmethod
    def _list_relations(tx, db_name):
        result = tx.run("USE {name} MATCH (n) RETURN n LIMIT 5".format(name=db_name))
        return result


def get_properties(self):
    return self._properties


def set_properties(node):
    if node:
        node.get_properties = types.MethodType(get_properties, node)
    return node


if __name__ == "__main__":
    network = CoOccurrenceManager("bolt://localhost:7687", "neo4j", "perdekj", "neo4j")
    # network = CoOccurrenceManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
    # network.create_db_for_network()
    network.get_data()
    network.close()
