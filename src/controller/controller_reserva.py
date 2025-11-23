from model.reserva import Reserva
from model.hospede import Hospede
from model.quarto import Quarto
from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Reserva:
    def __init__(self):
        self.mongo = MongoQueries(database="hotel_reservas")

    def quarto_disponivel(self, numero_quarto, checkin, checkout):
        """Retorna True se não houver reservas em conflito."""
        conflitos = self.mongo.db["reserva"].find({
            "numero_quarto": numero_quarto,
            "$or": [
                {"data_checkin": {"$lte": checkout}, "data_checkout": {"$gte": checkin}}
            ]
        })
        return len(list(conflitos)) == 0

    def inserir_reserva(self) -> Reserva:
        self.mongo.connect()

        
        hospedes = list(self.mongo.db["hospede"].find({}, {"_id": 0}))
        if len(hospedes) == 0:
            print("\nNão há hóspedes cadastrados.\n")
            self.mongo.close()
            return None

        for i, h in enumerate(hospedes, start=1):
            print(f"{i}) CPF: {h['cpf']} - Nome: {h['nome']}")
        idx = int(input("Selecione o hóspede: ")) - 1
        cpf = hospedes[idx]["cpf"]

        
        quartos = list(self.mongo.db["quarto"].find({}, {"_id": 0}))
        if len(quartos) == 0:
            print("\nNão há quartos cadastrados.\n")
            self.mongo.close()
            return None

        for i, q in enumerate(quartos, start=1):
            print(f"{i}) Número: {q['numero_quarto']} - Tipo: {q['tipo']} - Status: {q['status']}")
        idx = int(input("Selecione o quarto: ")) - 1
        numero_quarto = quartos[idx]["numero_quarto"]

        
        data_checkin = input("Data de check-in (AAAA-MM-DD): ")
        data_checkout = input("Data de check-out (AAAA-MM-DD): ")

        
        if not self.quarto_disponivel(numero_quarto, data_checkin, data_checkout):
            print("\n O quarto está indisponível para as datas informadas.\n")
            self.mongo.close()
            return None

        qtd_hospedes = int(input("Quantidade de hóspedes: "))

        
        quarto = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto})
        valor_diaria = float(quarto["valor_diaria"])

        dias = (datetime.strptime(data_checkout, "%Y-%m-%d") -
                datetime.strptime(data_checkin, "%Y-%m-%d")).days

        valor_total = dias * valor_diaria

        ultima = list(self.mongo.db["reserva"].find({}, {"_id": 0}).sort("id_reserva", -1).limit(1))
        novo_id = 1 if len(ultima) == 0 else int(ultima[0]["id_reserva"]) + 1

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

        self.mongo.db["reserva"].insert_one(documento)

        reserva = Reserva(
            novo_id,
            Hospede(cpf),
            Quarto(numero_quarto),
            data_checkin,
            data_checkout,
            qtd_hospedes,
            valor_total,
            "Ativa",
            documento["criado_em"]
        )

        print("\nReserva inserida com sucesso!\n")
        print(reserva.to_string())

        self.mongo.close()
        return reserva

    def atualizar_reserva(self) -> Reserva:
        self.mongo.connect()

        reserva_id = int(input("ID da reserva que deseja atualizar: "))

        doc = self.mongo.db["reserva"].find_one({"id_reserva": reserva_id})

        if not doc:
            print("\nReserva não encontrada.\n")
            self.mongo.close()
            return None

        print("\nDeixe em branco para não alterar.\n")

        data_checkin = input(f"Novo check-in ({doc['data_checkin']}): ") or doc["data_checkin"]
        data_checkout = input(f"Novo check-out ({doc['data_checkout']}): ") or doc["data_checkout"]
        qtd_hospedes = input(f"Nova qtd hóspedes ({doc['qtd_hospedes']}): ") or doc["qtd_hospedes"]
        status = input(f"Novo status ({doc['status']}): ") or doc["status"]

        
        quarto = self.mongo.db["quarto"].find_one({"numero_quarto": doc["numero_quarto"]})
        valor_diaria = quarto["valor_diaria"]

        dias = (datetime.strptime(data_checkout, "%Y-%m-%d") -
                datetime.strptime(data_checkin, "%Y-%m-%d")).days

        valor_total = dias * valor_diaria

        self.mongo.db["reserva"].update_one(
            {"id_reserva": reserva_id},
            {"$set": {
                "data_checkin": data_checkin,
                "data_checkout": data_checkout,
                "qtd_hospedes": int(qtd_hospedes),
                "valor_total": valor_total,
                "status": status
            }}
        )

        atualizado = self.mongo.db["reserva"].find_one({"id_reserva": reserva_id}, {"_id": 0})

        reserva = Reserva(
            atualizado["id_reserva"],
            Hospede(atualizado["cpf"]),
            Quarto(atualizado["numero_quarto"]),
            atualizado["data_checkin"],
            atualizado["data_checkout"],
            atualizado["qtd_hospedes"],
            atualizado["valor_total"],
            atualizado["status"],
            atualizado["criado_em"]
        )

        print("\nReserva atualizada com sucesso!\n")
        print(reserva.to_string())

        self.mongo.close()
        return reserva

    def excluir_reserva(self):
        self.mongo.connect()

        reserva_id = int(input("ID da reserva que deseja excluir: "))

        doc = self.mongo.db["reserva"].find_one({"id_reserva": reserva_id}, {"_id": 0})

        if not doc:
            print("\nReserva não encontrada.\n")
            self.mongo.close()
            return

        self.mongo.db["reserva"].delete_one({"id_reserva": reserva_id})

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

        self.mongo.close()

    def excluir_reserva_interactive(self):
        self.mongo.connect()

        reservas = list(self.mongo.db["reserva"].find({}, {"_id": 0}))

        if len(reservas) == 0:
            print("Nenhuma reserva cadastrada.")
            self.mongo.close()
            return

        for i, r in enumerate(reservas, start=1):
            print(f"{i}) ID: {r['id_reserva']} - CPF: {r['cpf']} - Quarto: {r['numero_quarto']}")

        idx = int(input("Selecione a reserva: ")) - 1
        reserva_id = reservas[idx]["id_reserva"]

        doc = self.mongo.db["reserva"].find_one({"id_reserva": reserva_id}, {"_id": 0})

        self.mongo.db["reserva"].delete_one({"id_reserva": reserva_id})

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

        self.mongo.close()
