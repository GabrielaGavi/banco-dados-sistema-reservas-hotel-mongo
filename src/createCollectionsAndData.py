import logging
import json
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries


LIST_OF_COLLECTIONS = ["hospede", "quarto", "reserva"]


logger = logging.getLogger(name="Sistema_Reservas_Hotel_MongoDB")
logger.setLevel(level=logging.WARNING)


mongo = MongoQueries(database="hotel_reservas")


def createCollections(drop_if_exists: bool = False):
    mongo.connect()
    existing_collections = mongo.db.list_collection_names()

    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} droped!")
                mongo.db.create_collection(collection)
                logger.warning(f"{collection} created!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")

    mongo.close()


def insert_many(data: json, collection: str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()


def extract_and_insert():
    oracle = OracleQueries()
    oracle.connect()

    
    queries = {
        "hospede": "SELECT cpf, nome, telefone, data_cadastro FROM hospede",
        "quarto": "SELECT numero_quarto, tipo, valor_diaria, status FROM quarto",
        "reserva": """SELECT id_reserva, cpf, numero_quarto,
                             data_checkin, data_checkout,
                             qtd_hospedes, valor_total, status, criado_em
                      FROM reserva"""
    }

    for collection in LIST_OF_COLLECTIONS:
        df = oracle.sqlToDataFrame(queries[collection])

        
        for col in df.columns:
            if "date" in str(df[col].dtype).lower() or "datetime" in str(df[col].dtype).lower():
                df[col] = df[col].astype(str)

        logger.warning(f"data extracted from Oracle.{collection}")

        
        records = json.loads(df.T.to_json()).values()
        logger.warning("data converted to json")

        
        insert_many(data=records, collection=collection)
        logger.warning(f"documents generated at {collection} collection")


if __name__ == "__main__":
    logging.warning("Starting migration")
    createCollections(drop_if_exists=True)
    extract_and_insert()
    logging.warning("End migration")
