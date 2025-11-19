from model.quarto import Quarto
from conexion.oracle_queries import OracleQueries

class Controller_Quarto:
    def __init__(self):
        pass
        
    def inserir_quarto(self) -> Quarto:
        
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        numero_quarto = input("Número do quarto (Novo): ")

        if self.verifica_existencia_quarto(oracle, numero_quarto):
            tipo = input("Tipo do quarto (ex: Solteiro, Casal, Suíte): ")
            valor_diaria = float(input("Valor da diária (ex: 200.00): "))
            status = input("Status (Disponível/Ocupado/Manutenção): ")

            oracle.write(f"""
                INSERT INTO quarto (numero_quarto, tipo, valor_diaria, status)
                VALUES ({numero_quarto}, '{tipo}', {valor_diaria}, '{status}')
            """)

            df_quarto = oracle.sqlToDataFrame(f"""
                SELECT numero_quarto, tipo, valor_diaria, status
                FROM quarto
                WHERE numero_quarto = {numero_quarto}
            """)

            novo_quarto = Quarto(
                df_quarto.numero_quarto.values[0],
                df_quarto.tipo.values[0],
                df_quarto.valor_diaria.values[0],
                df_quarto.status.values[0]
            )
            print("\nQuarto inserido com sucesso!\n")
            print(novo_quarto.to_string())
            return novo_quarto
        else:
            print(f"\nO quarto número {numero_quarto} já está cadastrado.\n")
            return None

    def atualizar_quarto(self) -> Quarto:
        

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        numero_quarto = input("Número do quarto que deseja atualizar: ")

        if not self.verifica_existencia_quarto(oracle, numero_quarto):
            tipo = input("Novo tipo: ")
            valor_diaria = float(input("Novo valor da diária: "))
            status = input("Novo status: ")

            oracle.write(f"""
                UPDATE quarto
                SET tipo = '{tipo}', valor_diaria = {valor_diaria}, status = '{status}'
                WHERE numero_quarto = {numero_quarto}
            """)

            df_quarto = oracle.sqlToDataFrame(f"""
                SELECT numero_quarto, tipo, valor_diaria, status
                FROM quarto
                WHERE numero_quarto = {numero_quarto}
            """)

            quarto_atualizado = Quarto(
                df_quarto.numero_quarto.values[0],
                df_quarto.tipo.values[0],
                df_quarto.valor_diaria.values[0],
                df_quarto.status.values[0]
            )
            print("\nQuarto atualizado com sucesso!\n")
            print(quarto_atualizado.to_string())
            return quarto_atualizado
        else:
            print(f"\nO quarto número {numero_quarto} não existe.\n")
            return None

    
    def atualizar_quarto_interactive(self) -> Quarto:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df = oracle.sqlToDataFrame("SELECT numero_quarto, tipo FROM quarto ORDER BY numero_quarto")
        if df.empty:
            print("Nenhum quarto cadastrado.")
            return None

        for i, row in enumerate(df.itertuples(), start=1):
            print(f"{i}) Nº: {row.numero_quarto} - Tipo: {row.tipo}")

        escolha = input("Selecione o número da tupla que deseja atualizar: ")
        try:
            idx = int(escolha) - 1
            numero_quarto = df.numero_quarto.values[idx]
        except Exception:
            print("Seleção inválida")
            return None

        escolha_attr = input("Atualizar todos os atributos? (S para sim / N para escolher um): ").strip().upper()
        if escolha_attr == 'S':
            tipo = input("Novo tipo: ")
            valor_diaria = float(input("Novo valor da diária: "))
            status = input("Novo status: ")
            oracle.write(f"""
                UPDATE quarto
                SET tipo = '{tipo}', valor_diaria = {valor_diaria}, status = '{status}'
                WHERE numero_quarto = {numero_quarto}
            """)
        else:
            print("Escolha o atributo:\n1) tipo\n2) valor_diaria\n3) status")
            opt = input("Opção: ")
            if opt == '1':
                tipo = input("Novo tipo: ")
                oracle.write(f"UPDATE quarto SET tipo = '{tipo}' WHERE numero_quarto = {numero_quarto}")
            elif opt == '2':
                valor_diaria = float(input("Novo valor da diária: "))
                oracle.write(f"UPDATE quarto SET valor_diaria = {valor_diaria} WHERE numero_quarto = {numero_quarto}")
            elif opt == '3':
                status = input("Novo status: ")
                oracle.write(f"UPDATE quarto SET status = '{status}' WHERE numero_quarto = {numero_quarto}")
            else:
                print("Opção inválida")
                return None

        df_quarto = oracle.sqlToDataFrame(f"SELECT numero_quarto, tipo, valor_diaria, status FROM quarto WHERE numero_quarto = {numero_quarto}")
        quarto_atualizado = Quarto(
            df_quarto.numero_quarto.values[0],
            df_quarto.tipo.values[0],
            df_quarto.valor_diaria.values[0],
            df_quarto.status.values[0]
        )
        print("\nQuarto atualizado com sucesso!\n")
        print(quarto_atualizado.to_string())
        return quarto_atualizado

    
    def excluir_quarto_interactive(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df = oracle.sqlToDataFrame("SELECT numero_quarto, tipo FROM quarto ORDER BY numero_quarto")
        if df.empty:
            print("Nenhum quarto cadastrado.")
            return

        for i, row in enumerate(df.itertuples(), start=1):
            print(f"{i}) Nº: {row.numero_quarto} - Tipo: {row.tipo}")

        escolha = input("Selecione o número da tupla que deseja excluir: ")
        try:
            idx = int(escolha) - 1
            numero_quarto = df.numero_quarto.values[idx]
        except Exception:
            print("Seleção inválida")
            return

        df_reserva = oracle.sqlToDataFrame(f"SELECT id_reserva FROM reserva WHERE numero_quarto = {numero_quarto}")
        if not df_reserva.empty:
            print(f"Não é possível excluir: o quarto {numero_quarto} possui reservas vinculadas.")
            resp = input("Deseja excluir também as reservas vinculadas? (S/N): ").strip().upper()
            if resp != 'S':
                print("Operação cancelada. Voltando ao menu.")
                return
            else:
                oracle.write(f"DELETE FROM reserva WHERE numero_quarto = {numero_quarto}")

        df_quarto = oracle.sqlToDataFrame(f"SELECT numero_quarto, tipo, valor_diaria, status FROM quarto WHERE numero_quarto = {numero_quarto}")
        oracle.write(f"DELETE FROM quarto WHERE numero_quarto = {numero_quarto}")

        quarto_excluido = Quarto(
            df_quarto.numero_quarto.values[0],
            df_quarto.tipo.values[0],
            df_quarto.valor_diaria.values[0],
            df_quarto.status.values[0]
        )
        print("\nQuarto removido com sucesso!\n")
        print(quarto_excluido.to_string())

    def excluir_quarto(self):
        
        
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        numero_quarto = input("Número do quarto que deseja excluir: ")

        if not self.verifica_existencia_quarto(oracle, numero_quarto):
            
            df_reserva = oracle.sqlToDataFrame(f"SELECT * FROM reserva WHERE numero_quarto = {numero_quarto}")
            if not df_reserva.empty:
                print(f"\nNão é possível excluir: o quarto {numero_quarto} possui reservas vinculadas.\n")
                return

            df_quarto = oracle.sqlToDataFrame(f"""
                SELECT numero_quarto, tipo, valor_diaria, status
                FROM quarto
                WHERE numero_quarto = {numero_quarto}
            """)
            oracle.write(f"DELETE FROM quarto WHERE numero_quarto = {numero_quarto}")

            quarto_excluido = Quarto(
                df_quarto.numero_quarto.values[0],
                df_quarto.tipo.values[0],
                df_quarto.valor_diaria.values[0],
                df_quarto.status.values[0]
            )
            print("\nQuarto removido com sucesso!\n")
            print(quarto_excluido.to_string())
        else:
            print(f"\nO quarto número {numero_quarto} não existe.\n")

    def verifica_existencia_quarto(self, oracle: OracleQueries, numero_quarto: int = None) -> bool:
        
        df_quarto = oracle.sqlToDataFrame(f"SELECT numero_quarto FROM quarto WHERE numero_quarto = {numero_quarto}")
        return df_quarto.empty
