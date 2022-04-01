import types
import neo4j


class NetworkManager:

    def __init__(self, uri, user, password, database_name='neo4j'):
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

    def process_data_transaction_without_arguments(self, used_function: any, db_name=None):
        if not db_name:
            db_name = self.database_name
        with self.driver.session() as session:
            creation = session.read_transaction(used_function, db_name)
            print(creation)
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

    def initialize_co_occurrence_indexes(self, db_name=None):
        if not db_name:
            db_name = self.database_name
        with self.driver.session() as session:
            creation = session.write_transaction(self._init_co_occurrence_indexes, db_name)
        return creation

    @staticmethod
    def _init_co_occurrence_indexes(tx, db_name):
        result1 = tx.run("""USE {name} CREATE TEXT INDEX idx_name1 IF NOT EXISTS 
                         FOR (n:Token) ON (n.name)""".format(name=db_name))
        result2 = tx.run("""USE {name} CREATE BTREE INDEX idx_name IF NOT EXISTS
                         FOR (n:Token) ON (n.name)""".format(name=db_name))
        return result1, result2

    def initialize_additional_indexes(self):
        try:
            with self.driver.session() as session:
                creation = session.write_transaction(self._init_additional_co_occurrence_indexes)
        except Exception as e:
            if "org.neo4j.kernel.api.exceptions.schema.EquivalentSchemaRuleAlreadyExistsException" in str(e):
                return None
            raise e
        return creation

    @staticmethod
    def _init_additional_co_occurrence_indexes(tx):
        result = tx.run("""CALL db.index.fulltext.createNodeIndex("nameLookup",["Token"],["name"])""")
        return result


def get_properties(self):
    return self._properties


def set_properties(node):
    if node:
        node.get_properties = types.MethodType(get_properties, node)
    return node


if __name__ == "__main__":
    network = NetworkManager("bolt://localhost:7687", "neo4j", "perdekj", "neo4j")
    # network = NetworkManager("bolt://localhost:7688", "neo4j", "neo4j1", "neo4j")
    # network.create_db_for_network()
    network.get_data()
    network.close()
