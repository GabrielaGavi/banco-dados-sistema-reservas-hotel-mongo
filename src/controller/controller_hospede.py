from model.hospede import Hospede
from conexion.oracle_queries import OracleQueries
from datetime import datetime

class Controller_Hospede:
    def __init__(self):
        pass
        
    def inserir_hospede(self) -> Hospede:
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_hospede(oracle, cpf):
            nome = input("Nome (Novo): ")
            telefone = input("Telefone (Novo): ")
            data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            
            oracle.write(f"""
                INSERT INTO hospede (cpf, nome, telefone, data_cadastro)
                VALUES ('{cpf}', '{nome}', '{telefone}', TO_DATE('{data_cadastro}', 'YYYY-MM-DD HH24:MI:SS'))
            """)

            
            df_hospede = oracle.sqlToDataFrame(f"SELECT cpf, nome, telefone, data_cadastro FROM hospede WHERE cpf = '{cpf}'")
            novo_hospede = Hospede(
                df_hospede.cpf.values[0],
                df_hospede.nome.values[0],
                df_hospede.telefone.values[0],
                str(df_hospede.data_cadastro.values[0])
            )
            print("\nHóspede inserido com sucesso!\n")
            print(novo_hospede.to_string())
            return novo_hospede
        else:
            print(f"\nO CPF {cpf} já está cadastrado.\n")
            return None

    def atualizar_hospede(self) -> Hospede:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = input("CPF do hóspede que deseja atualizar: ")

        if not self.verifica_existencia_hospede(oracle, cpf):
            nome = input("Novo nome: ")
            telefone = input("Novo telefone: ")
            data_cadastro = input("Nova data de cadastro (AAAA-MM-DD): ")

            oracle.write(f"""
                UPDATE hospede
                SET nome = '{nome}', telefone = '{telefone}', data_cadastro = TO_DATE('{data_cadastro}', 'YYYY-MM-DD')
                WHERE cpf = '{cpf}'
            """)

            df_hospede = oracle.sqlToDataFrame(f"SELECT cpf, nome, telefone, data_cadastro FROM hospede WHERE cpf = '{cpf}'")
            hospede_atualizado = Hospede(
                df_hospede.cpf.values[0],
                df_hospede.nome.values[0],
                df_hospede.telefone.values[0],
                str(df_hospede.data_cadastro.values[0])
            )
            print("\nHóspede atualizado com sucesso!\n")
            print(hospede_atualizado.to_string())
            return hospede_atualizado
        else:
            print(f"\nO CPF {cpf} não existe.\n")
            return None

    
    def atualizar_hospede_interactive(self) -> Hospede:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df = oracle.sqlToDataFrame("SELECT cpf, nome FROM hospede ORDER BY nome")
        if df.empty:
            print("Nenhum hóspede cadastrado.")
            return None

        for i, row in enumerate(df.itertuples(), start=1):
            print(f"{i}) CPF: {row.cpf} - Nome: {row.nome}")

        escolha = input("Selecione o número da tupla que deseja atualizar: ")
        try:
            idx = int(escolha) - 1
            cpf = df.cpf.values[idx]
        except Exception:
            print("Seleção inválida")
            return None

        
        escolha_attr = input("Atualizar todos os atributos? (S para sim / N para escolher um): ").strip().upper()
        if escolha_attr == 'S':
            nome = input("Novo nome: ")
            telefone = input("Novo telefone: ")
            data_cadastro = input("Nova data de cadastro (AAAA-MM-DD): ")
            oracle.write(f"""
                UPDATE hospede
                SET nome = '{nome}', telefone = '{telefone}', data_cadastro = TO_DATE('{data_cadastro}', 'YYYY-MM-DD')
                WHERE cpf = '{cpf}'
            """)
        else:
            print("Escolha o atributo:\n1) nome\n2) telefone\n3) data_cadastro")
            opt = input("Opção: ")
            if opt == '1':
                nome = input("Novo nome: ")
                oracle.write(f"UPDATE hospede SET nome = '{nome}' WHERE cpf = '{cpf}'")
            elif opt == '2':
                telefone = input("Novo telefone: ")
                oracle.write(f"UPDATE hospede SET telefone = '{telefone}' WHERE cpf = '{cpf}'")
            elif opt == '3':
                data_cadastro = input("Nova data de cadastro (AAAA-MM-DD): ")
                oracle.write(f"UPDATE hospede SET data_cadastro = TO_DATE('{data_cadastro}', 'YYYY-MM-DD') WHERE cpf = '{cpf}'")
            else:
                print("Opção inválida")
                return None

        df_hospede = oracle.sqlToDataFrame(f"SELECT cpf, nome, telefone, data_cadastro FROM hospede WHERE cpf = '{cpf}'")
        hospede_atualizado = Hospede(
            df_hospede.cpf.values[0],
            df_hospede.nome.values[0],
            df_hospede.telefone.values[0],
            str(df_hospede.data_cadastro.values[0])
        )
        print("\nHóspede atualizado com sucesso!\n")
        print(hospede_atualizado.to_string())
        return hospede_atualizado

    
    def excluir_hospede_interactive(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df = oracle.sqlToDataFrame("SELECT cpf, nome FROM hospede ORDER BY nome")
        if df.empty:
            print("Nenhum hóspede cadastrado.")
            return

        for i, row in enumerate(df.itertuples(), start=1):
            print(f"{i}) CPF: {row.cpf} - Nome: {row.nome}")

        escolha = input("Selecione o número da tupla que deseja excluir: ")
        try:
            idx = int(escolha) - 1
            cpf = df.cpf.values[idx]
        except Exception:
            print("Seleção inválida")
            return

        
        df_fk = oracle.sqlToDataFrame(f"SELECT id_reserva FROM reserva WHERE cpf = '{cpf}'")
        if not df_fk.empty:
            print(f"O hóspede com CPF {cpf} possui reservas vinculadas e não pode ser excluído automaticamente.")
            resp = input("Deseja excluir também as reservas vinculadas? (S/N): ").strip().upper()
            if resp != 'S':
                print("Operação cancelada. Voltando ao menu.")
                return
            else:
                
                oracle.write(f"DELETE FROM reserva WHERE cpf = '{cpf}'")

        df_hospede = oracle.sqlToDataFrame(f"SELECT cpf, nome, telefone, data_cadastro FROM hospede WHERE cpf = '{cpf}'")
        oracle.write(f"DELETE FROM hospede WHERE cpf = '{cpf}'")

        hospede_excluido = Hospede(
            df_hospede.cpf.values[0],
            df_hospede.nome.values[0],
            df_hospede.telefone.values[0],
            str(df_hospede.data_cadastro.values[0])
        )
        print("\nHóspede removido com sucesso!\n")
        print(hospede_excluido.to_string())

    def excluir_hospede(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = input("CPF do hóspede que deseja excluir: ")

        if not self.verifica_existencia_hospede(oracle, cpf):
            df_hospede = oracle.sqlToDataFrame(f"SELECT cpf, nome, telefone, data_cadastro FROM hospede WHERE cpf = '{cpf}'")
            oracle.write(f"DELETE FROM hospede WHERE cpf = '{cpf}'")

            hospede_excluido = Hospede(
                df_hospede.cpf.values[0],
                df_hospede.nome.values[0],
                df_hospede.telefone.values[0],
                str(df_hospede.data_cadastro.values[0])
            )
            print("\nHóspede removido com sucesso!\n")
            print(hospede_excluido.to_string())
        else:
            print(f"\nO CPF {cpf} não existe.\n")

    def verifica_existencia_hospede(self, oracle: OracleQueries, cpf: str = None) -> bool:
        df_hospede = oracle.sqlToDataFrame(f"SELECT cpf FROM hospede WHERE cpf = '{cpf}'")
        return df_hospede.empty
