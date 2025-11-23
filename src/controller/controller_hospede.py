from model.hospede import Hospede
from conexion.mongo_queries import MongoQueries
from datetime import datetime

class Controller_Hospede:
    def __init__(self):
        pass

    def inserir_hospede(self) -> Hospede:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_hospede(cpf):
            print(f"\nO CPF {cpf} já está cadastrado.\n")
            mongo.close()
            return None

        nome = input("Nome (Novo): ")
        telefone = input("Telefone (Novo): ")

        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        documento = {
            "cpf": cpf,
            "nome": nome,
            "telefone": telefone,
            "data_cadastro": data_cadastro
        }

        mongo.db["hospede"].insert_one(documento)
        mongo.close()

        novo = Hospede(cpf, nome, telefone, data_cadastro)

        print("\nHóspede inserido com sucesso!\n")
        print(novo.to_string())
        return novo


    def atualizar_hospede(self) -> Hospede:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        cpf = input("CPF do hóspede que deseja atualizar: ")

        if not self.verifica_existencia_hospede(cpf):
            print(f"\nO CPF {cpf} não existe.\n")
            mongo.close()
            return None

        nome = input("Novo nome: ")
        telefone = input("Novo telefone: ")
        data_cadastro = input("Nova data de cadastro (AAAA-MM-DD): ")

        mongo.db["hospede"].update_one(
            {"cpf": cpf},
            {"$set": {
                "nome": nome,
                "telefone": telefone,
                "data_cadastro": data_cadastro
            }}
        )

        doc = mongo.db["hospede"].find_one({"cpf": cpf}, {"_id": 0})
        mongo.close()

        atualizado = Hospede(doc["cpf"], doc["nome"], doc["telefone"], doc["data_cadastro"])

        print("\nHóspede atualizado com sucesso!\n")
        print(atualizado.to_string())
        return atualizado

    
    def atualizar_hospede_interactive(self) -> Hospede:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        hospedes = list(mongo.db["hospede"].find({}, {"_id": 0}).sort("nome", 1))

        if len(hospedes) == 0:
            print("Nenhum hóspede cadastrado.")
            mongo.close()
            return None

        for i, h in enumerate(hospedes, start=1):
            print(f"{i}) CPF: {h['cpf']} - Nome: {h['nome']}")

        escolha = input("Selecione o número da tupla que deseja atualizar: ")
        try:
            idx = int(escolha) - 1
            cpf = hospedes[idx]["cpf"]
        except:
            print("Seleção inválida.")
            mongo.close()
            return None

        escolha_attr = input("Atualizar todos os atributos? (S/N): ").strip().upper()

        if escolha_attr == "S":
            nome = input("Novo nome: ")
            telefone = input("Novo telefone: ")
            data_cadastro = input("Nova data de cadastro (AAAA-MM-DD): ")
            mongo.db["hospede"].update_one(
                {"cpf": cpf},
                {"$set": {"nome": nome, "telefone": telefone, "data_cadastro": data_cadastro}}
            )
        else:
            print("Escolha o atributo:\n1) Nome\n2) Telefone\n3) Data de Cadastro")
            opt = input("Opção: ")

            if opt == "1":
                valor = input("Novo nome: ")
                mongo.db["hospede"].update_one({"cpf": cpf}, {"$set": {"nome": valor}})
            elif opt == "2":
                valor = input("Novo telefone: ")
                mongo.db["hospede"].update_one({"cpf": cpf}, {"$set": {"telefone": valor}})
            elif opt == "3":
                valor = input("Nova data de cadastro: ")
                mongo.db["hospede"].update_one({"cpf": cpf}, {"$set": {"data_cadastro": valor}})
            else:
                print("Opção inválida.")
                mongo.close()
                return None

        doc = mongo.db["hospede"].find_one({"cpf": cpf}, {"_id": 0})
        mongo.close()

        atualizado = Hospede(doc["cpf"], doc["nome"], doc["telefone"], doc["data_cadastro"])

        print("\nHóspede atualizado com sucesso!\n")
        print(atualizado.to_string())
        return atualizado

   
    def excluir_hospede_interactive(self):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        hospedes = list(mongo.db["hospede"].find({}, {"_id": 0}).sort("nome", 1))

        if len(hospedes) == 0:
            print("Nenhum hóspede cadastrado.")
            mongo.close()
            return

        for i, h in enumerate(hospedes, start=1):
            print(f"{i}) CPF: {h['cpf']} - Nome: {h['nome']}")

        escolha = input("Selecione o número da tupla que deseja excluir: ")
        try:
            idx = int(escolha) - 1
            cpf = hospedes[idx]["cpf"]
        except:
            print("Seleção inválida.")
            mongo.close()
            return

        reservas = list(mongo.db["reserva"].find({"cpf": cpf}))
        if len(reservas) > 0:
            print(f"O hóspede CPF {cpf} possui reservas vinculadas.")
            resp = input("Deseja excluir também as reservas? (S/N): ").strip().upper()
            if resp == "S":
                mongo.db["reserva"].delete_many({"cpf": cpf})
            else:
                print("Operação cancelada.")
                mongo.close()
                return

        doc = mongo.db["hospede"].find_one({"cpf": cpf}, {"_id": 0})
        mongo.db["hospede"].delete_one({"cpf": cpf})
        mongo.close()

        excluido = Hospede(doc["cpf"], doc["nome"], doc["telefone"], doc["data_cadastro"])

        print("\nHóspede removido com sucesso!\n")
        print(excluido.to_string())

    
    def excluir_hospede(self):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        cpf = input("CPF do hóspede que deseja excluir: ")

        if not self.verifica_existencia_hospede(cpf):
            print(f"\nO CPF {cpf} não existe.\n")
            mongo.close()
            return

        doc = mongo.db["hospede"].find_one({"cpf": cpf}, {"_id": 0})
        mongo.db["hospede"].delete_one({"cpf": cpf})
        mongo.close()

        excluido = Hospede(doc["cpf"], doc["nome"], doc["telefone"], doc["data_cadastro"])

        print("\nHóspede removido com sucesso!\n")
        print(excluido.to_string())

    def verifica_existencia_hospede(self, cpf: str) -> bool:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()
        existe = mongo.db["hospede"].find_one({"cpf": cpf}) is not None
        mongo.close()
        return existe
