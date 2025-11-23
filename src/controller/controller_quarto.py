from model.quarto import Quarto
from conexion.mongo_queries import MongoQueries

class Controller_Quarto:
    def __init__(self):
        self.mongo = MongoQueries(database="hotel_reservas")

    def inserir_quarto(self) -> Quarto:
        self.mongo.connect()

        numero_quarto = int(input("Número do quarto (Novo): "))

        if not self.verifica_existencia_quarto(numero_quarto):
            tipo = input("Tipo (Novo): ")
            valor_diaria = float(input("Valor da diária (Novo): "))
            status = input("Status (Disponível, Ocupado, Em Limpeza): ")

            documento = {
                "numero_quarto": numero_quarto,
                "tipo": tipo,
                "valor_diaria": valor_diaria,
                "status": status
            }

            self.mongo.db["quarto"].insert_one(documento)

            novo_quarto = Quarto(
                numero_quarto,
                tipo,
                valor_diaria,
                status
            )

            print("\nQuarto inserido com sucesso!\n")
            print(novo_quarto.to_string())

            self.mongo.close()
            return novo_quarto
        else:
            print(f"\nO quarto {numero_quarto} já está cadastrado.\n")
            self.mongo.close()
            return None
        
    def atualizar_quarto(self) -> Quarto:
        self.mongo.connect()

        numero_quarto = int(input("Número do quarto que deseja atualizar: "))

        if self.verifica_existencia_quarto(numero_quarto):
            tipo = input("Novo tipo: ")
            valor_diaria = float(input("Novo valor da diária: "))
            status = input("Novo status (Disponível/Ocupado/Em Limpeza): ")

            self.mongo.db["quarto"].update_one(
                {"numero_quarto": numero_quarto},
                {"$set": {
                    "tipo": tipo,
                    "valor_diaria": valor_diaria,
                    "status": status
                }}
            )

            doc = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
            quarto = Quarto(
                doc["numero_quarto"],
                doc["tipo"],
                doc["valor_diaria"],
                doc["status"]
            )

            print("\nQuarto atualizado com sucesso!\n")
            print(quarto.to_string())

            self.mongo.close()
            return quarto

        else:
            print(f"\nO quarto {numero_quarto} não existe.\n")
            self.mongo.close()
            return None

    def atualizar_quarto_interactive(self) -> Quarto:
        self.mongo.connect()

        quartos = list(self.mongo.db["quarto"].find({}, {"_id": 0}).sort("numero_quarto", 1))

        if len(quartos) == 0:
            print("Nenhum quarto cadastrado.")
            self.mongo.close()
            return None

        
        for i, q in enumerate(quartos, start=1):
            print(f"{i}) Número: {q['numero_quarto']} - Tipo: {q['tipo']} - Status: {q['status']}")

        escolha = input("Selecione o número da tupla que deseja atualizar: ")

        try:
            idx = int(escolha) - 1
            numero_quarto = quartos[idx]["numero_quarto"]
        except:
            print("Seleção inválida.")
            self.mongo.close()
            return None

        escolha_attr = input("Atualizar todos os atributos? (S/N): ").strip().upper()

        if escolha_attr == "S":
            tipo = input("Novo tipo: ")
            valor_diaria = float(input("Novo valor da diária: "))
            status = input("Novo status: ")

            self.mongo.db["quarto"].update_one(
                {"numero_quarto": numero_quarto},
                {"$set": {
                    "tipo": tipo,
                    "valor_diaria": valor_diaria,
                    "status": status
                }}
            )
        else:
            print("Escolha o atributo:\n1) tipo\n2) valor_diaria\n3) status")
            opt = input("Opção: ")

            if opt == '1':
                valor = input("Novo tipo: ")
                self.mongo.db["quarto"].update_one({"numero_quarto": numero_quarto}, {"$set": {"tipo": valor}})
            elif opt == '2':
                valor = float(input("Novo valor da diária: "))
                self.mongo.db["quarto"].update_one({"numero_quarto": numero_quarto}, {"$set": {"valor_diaria": valor}})
            elif opt == '3':
                valor = input("Novo status: ")
                self.mongo.db["quarto"].update_one({"numero_quarto": numero_quarto}, {"$set": {"status": valor}})
            else:
                print("Opção inválida.")
                self.mongo.close()
                return None

        doc = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
        atualizado = Quarto(
            doc["numero_quarto"],
            doc["tipo"],
            doc["valor_diaria"],
            doc["status"]
        )

        print("\nQuarto atualizado com sucesso!\n")
        print(atualizado.to_string())

        self.mongo.close()
        return atualizado

    def excluir_quarto_interactive(self):
        self.mongo.connect()

        quartos = list(self.mongo.db["quarto"].find({}, {"_id": 0}).sort("numero_quarto", 1))

        if len(quartos) == 0:
            print("Nenhum quarto cadastrado.")
            self.mongo.close()
            return

        for i, q in enumerate(quartos, start=1):
            print(f"{i}) Número: {q['numero_quarto']} - Tipo: {q['tipo']}")

        escolha = input("Selecione o número da tupla que deseja excluir: ")

        try:
            idx = int(escolha) - 1
            numero_quarto = quartos[idx]["numero_quarto"]
        except:
            print("Seleção inválida.")
            self.mongo.close()
            return

        
        reservas = list(self.mongo.db["reserva"].find({"numero_quarto": numero_quarto}))
        if len(reservas) > 0:
            print("Este quarto possui reservas vinculadas.")
            resp = input("Deseja excluir todas as reservas vinculadas? (S/N): ").strip().upper()
            if resp != "S":
                print("Operação cancelada.")
                self.mongo.close()
                return
            else:
                self.mongo.db["reserva"].delete_many({"numero_quarto": numero_quarto})

        doc = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})

        self.mongo.db["quarto"].delete_one({"numero_quarto": numero_quarto})

        excluido = Quarto(
            doc["numero_quarto"],
            doc["tipo"],
            doc["valor_diaria"],
            doc["status"]
        )

        print("\nQuarto removido com sucesso!\n")
        print(excluido.to_string())

        self.mongo.close()
        
    def excluir_quarto(self):
        self.mongo.connect()

        numero_quarto = int(input("Número do quarto que deseja excluir: "))

        if self.verifica_existencia_quarto(numero_quarto):
            doc = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}, {"_id": 0})
            self.mongo.db["quarto"].delete_one({"numero_quarto": numero_quarto})

            excluido = Quarto(
                doc["numero_quarto"],
                doc["tipo"],
                doc["valor_diaria"],
                doc["status"]
            )

            print("\nQuarto removido com sucesso!\n")
            print(excluido.to_string())
        else:
            print(f"\nO quarto {numero_quarto} não existe.\n")

        self.mongo.close()

    def verifica_existencia_quarto(self, numero_quarto: int) -> bool:
        self.mongo.connect()
        existe = self.mongo.db["quarto"].find_one({"numero_quarto": numero_quarto}) is not None
        self.mongo.close()
        return existe
