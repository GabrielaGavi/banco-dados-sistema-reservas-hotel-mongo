from model.reserva import Reserva
from model.hospede import Hospede
from model.quarto import Quarto
from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Reserva:
    def __init__(self):
        pass

    def quarto_disponivel(self, numero_quarto, checkin, checkout):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        conflitos = list(mongo.db["reserva"].find({
            "numero_quarto": numero_quarto,
            "$or": [
                {
                    "data_checkin": {"$lte": checkout},
                    "data_checkout": {"$gte": checkin}
                }
            ]
        }))

        mongo.close()
        return len(conflitos) == 0

    def inserir_reserva(self) -> Reserva:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        
        hospedes = list(mongo.db["hospede"].find({}, {"_id": 0}))
        if len(hospedes) == 0:
            print("Nenhum hóspede cadastrado.")
            mongo.close()
            return None

        for i, h in enumerate(hospedes, start=1):
            print(f"{i}) CPF: {h['cpf']} - Nome: {h['nome']}")

        idx = int(input("Selecione o hóspede: ")) - 1
        cpf = hospedes[idx]["cpf"]

        
        quartos = list(mongo.db["quarto"].find({}, {"_id": 0}))
        if len(quartos) == 0:
            print("Nenhum quarto cadastrado.")
            mongo.close()
            return None

        for i, q in enumerate(quartos, start=1):
            print(f"{i}) Número: {q['numero_quarto']} - Tipo: {q['tipo']} - Status: {q['status']}")

        idx = int(input("Selecione o quarto: ")) - 1
        numero_quarto = quartos[idx]["numero_quarto"]

        
        data_checkin = input("Data check-in (AAAA-MM-DD): ")
        data_checkout = input("Data check-out (AAAA-MM-DD): ")

        
        if not self.quarto_disponivel(numero_quarto, data_checkin, data_checkout):
            print("\nO quarto está indisponível para as datas informadas.\n")
            mongo.close()
            return None

        qtd_hospedes = int(input("Quantidade de hóspedes: "))

        
        doc_quarto = mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
        valor_diaria = doc_quarto["valor_diaria"]

        dias = (datetime.strptime(data_checkout, "%Y-%m-%d") -
                datetime.strptime(data_checkin, "%Y-%m-%d")).days

        valor_total = dias * valor_diaria

        ultima = list(mongo.db["reserva"].find({}, {"_id": 0}).sort("id_reserva", -1).limit(1))
        novo_id = 1 if len(ultima) == 0 else ultima[0]["id_reserva"] + 1

        documento = {
            "id_reserva": novo_id,
            "cpf": cpf,
            "numero_quarto": numero_quarto,
            "data_checkin": data_checkin,
            "data_checkout": data_checkout,
            "qtd_hospedes": qtd_hospedes,
            "valor_total": valor_total,
            "status": "Ativa",
            "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        mongo.db["reserva"].insert_one(documento)

        mongo.db["quarto"].update_one(
            {"numero_quarto": numero_quarto},
            {"$set": {"status": "Ocupado"}}
        )

        
        doc_hospede = mongo.db["hospede"].find_one({"cpf": cpf}, {"_id": 0})
        hospede_obj = Hospede(
            doc_hospede["cpf"],
            doc_hospede["nome"],
            doc_hospede["telefone"],
            doc_hospede["data_cadastro"]
        )

        
        quarto_obj = Quarto(
            doc_quarto["numero_quarto"],
            doc_quarto["tipo"],
            doc_quarto["valor_diaria"],
            "Ocupado"
        )

        mongo.close()

        reserva = Reserva(
            novo_id,
            hospede_obj,
            quarto_obj,
            data_checkin,
            data_checkout,
            qtd_hospedes,
            valor_total,
            "Ativa",
            documento["criado_em"]
        )

        print("\nReserva inserida com sucesso!\n")
        print(reserva.to_string())
        return reserva

    def atualizar_reserva(self) -> Reserva:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        reserva_id = int(input("ID da reserva que deseja atualizar: "))

        doc = mongo.db["reserva"].find_one({"id_reserva": reserva_id})
        if not doc:
            print("Reserva não encontrada.")
            mongo.close()
            return None

        print("\nDeixe em branco para manter o valor atual.\n")

        data_checkin = input(f"Novo check-in ({doc['data_checkin']}): ") or doc["data_checkin"]
        data_checkout = input(f"Novo check-out ({doc['data_checkout']}): ") or doc["data_checkout"]
        qtd_hospedes = int(input(f"Nova quantidade ({doc['qtd_hospedes']}): ") or doc["qtd_hospedes"])
        status = input(f"Novo status ({doc['status']}): ") or doc["status"]

        doc_quarto = mongo.db["quarto"].find_one({"numero_quarto": doc["numero_quarto"]})
        valor_diaria = doc_quarto["valor_diaria"]

        dias = (datetime.strptime(data_checkout, "%Y-%m-%d") -
                datetime.strptime(data_checkin, "%Y-%m-%d")).days

        valor_total = dias * valor_diaria

        mongo.db["reserva"].update_one(
            {"id_reserva": reserva_id},
            {"$set": {
                "data_checkin": data_checkin,
                "data_checkout": data_checkout,
                "qtd_hospedes": qtd_hospedes,
                "valor_total": valor_total,
                "status": status
            }}
        )

        atualizado = mongo.db["reserva"].find_one({"id_reserva": reserva_id}, {"_id": 0})

        doc_hospede = mongo.db["hospede"].find_one({"cpf": atualizado["cpf"]}, {"_id": 0})
        hospede_obj = Hospede(
            doc_hospede["cpf"],
            doc_hospede["nome"],
            doc_hospede["telefone"],
            doc_hospede["data_cadastro"]
        )

        quarto_obj = Quarto(
            doc_quarto["numero_quarto"],
            doc_quarto["tipo"],
            doc_quarto["valor_diaria"],
            doc_quarto["status"]
        )

        mongo.close()

        reserva = Reserva(
            atualizado["id_reserva"],
            hospede_obj,
            quarto_obj,
            atualizado["data_checkin"],
            atualizado["data_checkout"],
            atualizado["qtd_hospedes"],
            atualizado["valor_total"],
            atualizado["status"],
            atualizado["criado_em"]
        )

        print("\nReserva atualizada com sucesso!\n")
        print(reserva.to_string())
        return reserva

    def excluir_reserva(self):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        reserva_id = int(input("ID da reserva que deseja excluir: "))

        doc = mongo.db["reserva"].find_one({"id_reserva": reserva_id}, {"_id": 0})
        if not doc:
            print("Reserva não encontrada.")
            mongo.close()
            return

        mongo.db["quarto"].update_one(
            {"numero_quarto": doc["numero_quarto"]},
            {"$set": {"status": "Disponível"}}
        )

        mongo.db["reserva"].delete_one({"id_reserva": reserva_id})

        excluida = Reserva(
            doc["id_reserva"],
            Hospede(doc["cpf"]),
            Quarto(doc["numero_quarto"]),
            doc["data_checkin"],
            doc["data_checkout"],
            doc["qtd_hospedes"],
            doc["valor_total"],
            doc["status"],
            doc["criado_em"]
        )

        mongo.close()

        print("\nReserva removida com sucesso!\n")
        print(excluida.to_string())

    def excluir_reserva_interactive(self):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        reservas = list(mongo.db["reserva"].find({}, {"_id": 0}))
        if len(reservas) == 0:
            print("Nenhuma reserva cadastrada.")
            mongo.close()
            return

        for i, r in enumerate(reservas, start=1):
            print(f"{i}) ID: {r['id_reserva']} - CPF: {r['cpf']} - Quarto: {r['numero_quarto']}")

        idx = int(input("Selecione: ")) - 1
        reserva_id = reservas[idx]["id_reserva"]

        doc = mongo.db["reserva"].find_one({"id_reserva": reserva_id}, {"_id": 0})

        mongo.db["quarto"].update_one(
            {"numero_quarto": doc["numero_quarto"]},
            {"$set": {"status": "Disponível"}}
        )

        mongo.db["reserva"].delete_one({"id_reserva": reserva_id})
        mongo.close()

        excluida = Reserva(
            doc["id_reserva"],
            Hospede(doc["cpf"]),
            Quarto(doc["numero_quarto"]),
            doc["data_checkin"],
            doc["data_checkout"],
            doc["qtd_hospedes"],
            doc["valor_total"],
            doc["status"],
            doc["criado_em"]
        )

        print("\nReserva removida com sucesso!\n")
        print(excluida.to_string())
