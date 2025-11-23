from conexion.mongo_queries import MongoQueries
import pandas as pd

class Relatorios:
    def __init__(self):
        self.mongo = MongoQueries(database="hotel_reservas")

    def exibir_dataframe(self, dados):
        if len(dados) == 0:
            print("\n### Nenhum dado encontrado para este relatório. ###\n")
        else:
            df = pd.DataFrame(dados)
            print(df.to_string(index=False))

        input("\nPressione Enter para voltar ao menu...")

    def relatorio_reservas_por_status(self):
        self.mongo.connect()

        pipeline = [
            {"$group": {
                "_id": "$status",
                "total_reservas": {"$sum": 1},
                "soma_valores": {"$sum": "$valor_total"}
            }},
            {"$sort": {"total_reservas": -1}}
        ]

        resultado = list(self.mongo.db["reserva"].aggregate(pipeline))
        
        for r in resultado:
            r["status"] = r.pop("_id")

        print("\n### RELATÓRIO DE RESERVAS POR STATUS ###\n")
        self.exibir_dataframe(resultado)

        self.mongo.close()

    def relatorio_reservas_detalhado(self):
        self.mongo.connect()

        pipeline = [
            
            {
                "$lookup": {
                    "from": "hospede",
                    "localField": "cpf",
                    "foreignField": "cpf",
                    "as": "hospede_info"
                }
            },
            {"$unwind": "$hospede_info"},

            
            {
                "$lookup": {
                    "from": "quarto",
                    "localField": "numero_quarto",
                    "foreignField": "numero_quarto",
                    "as": "quarto_info"
                }
            },
            {"$unwind": "$quarto_info"},

            
            {"$project": {
                "_id": 0,
                "id_reserva": 1,
                "nome_hospede": "$hospede_info.nome",
                "tipo_quarto": "$quarto_info.tipo",
                "data_checkin": 1,
                "data_checkout": 1,
                "valor_total": 1,
                "status": 1
            }},

            {"$sort": {"data_checkin": 1}}
        ]

        resultado = list(self.mongo.db["reserva"].aggregate(pipeline))

        print("\n### RELATÓRIO DETALHADO DE RESERVAS ###\n")
        self.exibir_dataframe(resultado)

        self.mongo.close()

    def relatorio_reservas_por_mes(self):
        self.mongo.connect()

        pipeline = [
            
            {
                "$addFields": {
                    "mes_ano": {
                        "$substr": ["$criado_em", 0, 7]  # "YYYY-MM"
                    }
                }
            },
            {"$group": {
                "_id": "$mes_ano",
                "total_reservas": {"$sum": 1},
                "soma_valores": {"$sum": "$valor_total"}
            }},
            {"$sort": {"_id": 1}}
        ]

        resultado = list(self.mongo.db["reserva"].aggregate(pipeline))

        for r in resultado:
            r["mes_ano"] = r.pop("_id")

        print("\n### RELATÓRIO DE RESERVAS POR MÊS ###\n")
        self.exibir_dataframe(resultado)

        self.mongo.close()

    def relatorio_hospedes(self):
        self.mongo.connect()

        resultado = list(
            self.mongo.db["hospede"].find({}, {"_id": 0}).sort("nome", 1)
        )

        print("\n### RELATÓRIO DE HÓSPEDES ###\n")
        self.exibir_dataframe(resultado)

        self.mongo.close()
