from model.quarto import Quarto
from conexion.mongo_queries import MongoQueries

class Controller_Quarto:
    def __init__(self):
        pass

    def inserir_quarto(self) -> Quarto:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        numero_quarto = int(input("Número do quarto (Novo): "))

        if self.verifica_existencia_quarto(numero_quarto):
            print(f"\nO quarto {numero_quarto} já está cadastrado.\n")
            mongo.close()
            return None

        tipo = input("Tipo (Novo): ")
        valor_diaria = float(input("Valor da diária (Novo): "))
        status = input("Status (Disponível/Ocupado/Em Limpeza): ")

        documento = {
            "numero_quarto": numero_quarto,
            "tipo": tipo,
            "valor_diaria": valor_diaria,
            "status": status
        }

        mongo.db["quarto"].insert_one(documento)
        mongo.close()

        novo_quarto = Quarto(numero_quarto, tipo, valor_diaria, status)

        print("\nQuarto inserido com sucesso!\n")
        print(novo_quarto.to_string())
        return novo_quarto


    def atualizar_quarto(self) -> Quarto:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        numero_quarto = int(input("Número do quarto que deseja atualizar: "))

        if not self.verifica_existencia_quarto(numero_quarto):
            print(f"\nO quarto {numero_quarto} não existe.\n")
            mongo.close()
            return None

        tipo = input("Novo tipo: ")
        valor_diaria = float(input("Novo valor da diária: "))
        status = input("Novo status (Disponível/Ocupado/Em Limpeza): ")

        mongo.db["quarto"].update_one(
            {"numero_quarto": numero_quarto},
            {"$set": {
                "tipo": tipo,
                "valor_diaria": valor_diaria,
                "status": status
            }}
        )

        doc = mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
        mongo.close()

        quarto = Quarto(
            doc["numero_quarto"],
            doc["tipo"],
            doc["valor_diaria"],
            doc["status"]
        )

        print("\nQuarto atualizado com sucesso!\n")
        print(quarto.to_string())
        return quarto


    def atualizar_quarto_interactive(self) -> Quarto:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        quartos = list(mongo.db["quarto"].find({}, {"_id": 0}).sort("numero_quarto", 1))

        if len(quartos) == 0:
            print("Nenhum quarto cadastrado.")
            mongo.close()
            return None

        for i, q in enumerate(quartos, start=1):
            print(f"{i}) Número: {q['numero_quarto']} - Tipo: {q['tipo']} - Status: {q['status']}")

        escolha = input("Selecione o número da tupla que deseja atualizar: ")

        try:
            idx = int(escolha) - 1
            numero_quarto = quartos[idx]["numero_quarto"]
        except:
            print("Seleção inválida.")
            mongo.close()
            return None

        escolha_attr = input("Atualizar todos os atributos? (S/N): ").upper()

        if escolha_attr == "S":
            tipo = input("Novo tipo: ")
            valor_diaria = float(input("Novo valor da diária: "))
            status = input("Novo status: ")

            mongo.db["quarto"].update_one(
                {"numero_quarto": numero_quarto},
                {"$set": {
                    "tipo": tipo,
                    "valor_diaria": valor_diaria,
                    "status": status
                }}
            )
        else:
            print("Escolha o atributo:\n1) Tipo\n2) Valor da diária\n3) Status")
            opt = input("Opção: ")

            if opt == '1':
                valor = input("Novo tipo: ")
                mongo.db["quarto"].update_one({"numero_quarto": numero_quarto}, {"$set": {"tipo": valor}})
            elif opt == '2':
                valor = float(input("Novo valor da diária: "))
                mongo.db["quarto"].update_one({"numero_quarto": numero_quarto}, {"$set": {"valor_diaria": valor}})
            elif opt == '3':
                valor = input("Novo status: ")
                mongo.db["quarto"].update_one({"numero_quarto": numero_quarto}, {"$set": {"status": valor}})
            else:
                print("Opção inválida.")
                mongo.close()
                return None

        doc = mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
        mongo.close()

        atualizado = Quarto(
            doc["numero_quarto"],
            doc["tipo"],
            doc["valor_diaria"],
            doc["status"]
        )

        print("\nQuarto atualizado com sucesso!\n")
        print(atualizado.to_string())
        return atualizado

    def excluir_quarto_interactive(self):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        quartos = list(mongo.db["quarto"].find({}, {"_id": 0}).sort("numero_quarto", 1))

        if len(quartos) == 0:
            print("Nenhum quarto cadastrado.")
            mongo.close()
            return

        for i, q in enumerate(quartos, start=1):
            print(f"{i}) Número: {q['numero_quarto']} - Tipo: {q['tipo']}")

        escolha = input("Selecione o número da tupla que deseja excluir: ")

        try:
            idx = int(escolha) - 1
            numero_quarto = quartos[idx]["numero_quarto"]
        except:
            print("Seleção inválida.")
            mongo.close()
            return

        reservas = list(mongo.db["reserva"].find({"numero_quarto": numero_quarto}))
        if len(reservas) > 0:
            print("Este quarto possui reservas vinculadas.")
            resp = input("Deseja excluir todas as reservas vinculadas? (S/N): ").upper()
            if resp != "S":
                print("Operação cancelada.")
                mongo.close()
                return
            else:
                mongo.db["reserva"].delete_many({"numero_quarto": numero_quarto})

        doc = mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
        mongo.db["quarto"].delete_one({"numero_quarto": numero_quarto})
        mongo.close()

        excluido = Quarto(
            doc["numero_quarto"],
            doc["tipo"],
            doc["valor_diaria"],
            doc["status"]
        )

        print("\nQuarto removido com sucesso!\n")
        print(excluido.to_string())


    def excluir_quarto(self):
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()

        numero_quarto = int(input("Número do quarto que deseja excluir: "))

        if not self.verifica_existencia_quarto(numero_quarto):
            print(f"\nO quarto {numero_quarto} não existe.\n")
            mongo.close()
            return

        doc = mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
        mongo.db["quarto"].delete_one({"numero_quarto": numero_quarto})
        mongo.close()

        excluido = Quarto(
            doc["numero_quarto"],
            doc["tipo"],
            doc["valor_diaria"],
            doc["status"]
        )

        print("\nQuarto removido com sucesso!\n")
        print(excluido.to_string())

    
    def verifica_existencia_quarto(self, numero_quarto: int) -> bool:
        mongo = MongoQueries(database="hotel_reservas")
        mongo.connect()
        existe = mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}) is not None
        mongo.close()
        return existe
