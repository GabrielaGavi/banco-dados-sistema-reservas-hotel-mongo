from pymongo import MongoClient

class MongoQueries:
    def __init__(self, database: str = None):
    
        self.database = database
        self.client = None
        self.db = None

        
        with open("src/conexion/passphrase/authentication.mongo", "r") as f:
            self.connection_string = f.read().strip()

    def connect(self):
        try:
            
            self.client = MongoClient(self.connection_string)

            
            self.db = self.client[self.database]

            return self.db
        except Exception as e:
            print("\nErro ao conectar ao MongoDB:", e)
            return None

    def close(self):
        if self.client:
            self.client.close()

    def find_all(self, collection: str):
        
        return list(self.db[collection].find({}))

    def find(self, collection: str, filtro: dict):
        
        return list(self.db[collection].find(filtro))

    def insert(self, collection: str, documento: dict):
        
        return self.db[collection].insert_one(documento)

    def update(self, collection: str, filtro: dict, novos_valores: dict):
        
        return self.db[collection].update_one(filtro, {"$set": novos_valores})

    def delete(self, collection: str, filtro: dict):
        
        return self.db[collection].delete_one(filtro)

    def aggregate(self, collection: str, pipeline: list):
        
        return list(self.db[collection].aggregate(pipeline))
