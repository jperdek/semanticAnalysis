import os
try:
    from apis.http.api.graphProcessing.network_manager import NetworkManager
except ImportError:
    from serverParts.apis.http.api.graphProcessing.network_manager import NetworkManager


class CoOccurrenceNetworkManager(NetworkManager):
    def __init__(self):
        if "CO_OCCURRENCE_DB_NAME" in os.environ:
            self.database_name = os.environ["CO_OCCURRENCE_DB_NAME"]
        else:
            self.database_name = "neo4j"
        if "CO_OCCURRENCE_DB_USER" in os.environ:
            self.database_user = os.environ["CO_OCCURRENCE_DB_USER"]
        else:
            self.database_user = "neo4j"
        if "CO_OCCURRENCE_DB_PASSWORD" in os.environ:
            self.database_password = os.environ["CO_OCCURRENCE_DB_PASSWORD"]
        else:
            self.database_password = "neo4j1"
        if "CO_OCCURRENCE_DB_BOLT" in os.environ:
            self.database_bolt = os.environ["CO_OCCURRENCE_DB_BOLT"]
        else:
            self.database_bolt = "bolt://localhost:7688"
        super().__init__(self.database_bolt, self.database_user,
                         self.database_password, self.database_name)


class YagoNetworkManager(NetworkManager):
    def __init__(self):
        if "YAGO_DB_NAME" in os.environ:
            self.database_name = os.environ["YAGO_DB_NAME"]
        else:
            self.database_name = "neo4j"
        if "YAGO_DB_USER" in os.environ:
            self.database_user = os.environ["YAGO_DB_USER"]
        else:
            self.database_user = "neo4j"
        if "YAGO_DB_PASSWORD" in os.environ:
            self.database_password = os.environ["YAGO_DB_PASSWORD"]
        else:
            self.database_password = "perdekj"
        if "YAGO_DB_BOLT" in os.environ:
            self.database_bolt = os.environ["YAGO_DB_BOLT"]
        else:
            self.database_bolt = "bolt://localhost:7687"
        super().__init__(self.database_bolt, self.database_user,
                         self.database_password, self.database_name)
