from datetime import datetime
from model.reserva import Reserva
from model.hospede import Hospede
from model.quarto import Quarto
from conexion.oracle_queries import OracleQueries

class Controller_Reserva:
    def __init__(self):
        pass

    def inserir_reserva(self) -> Reserva:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        
        df_hospedes = oracle.sqlToDataFrame("SELECT cpf, nome FROM hospede ORDER BY nome")
        if df_hospedes.empty:
            print("Nenhum hóspede cadastrado. Cadastre um hóspede antes de criar uma reserva.")
            return None

        for i, row in enumerate(df_hospedes.itertuples(), start=1):
            print(f"{i}) CPF: {row.cpf} - Nome: {row.nome}")

        escolha = input("Selecione o número do hóspede ou digite o CPF diretamente: ").strip()
        cpf = None
        try:
            
            if escolha.isdigit():
                idx = int(escolha) - 1
                cpf = df_hospedes.cpf.values[idx]
            else:
                cpf = escolha
        except Exception:
            print("Seleção inválida.")
            return None

        numero_quarto = int(input("Número do quarto: "))
        data_checkin = input("Data de check-in (YYYY-MM-DD): ")
        data_checkout = input("Data de check-out (YYYY-MM-DD): ")
        qtd_hospedes = int(input("Quantidade de hóspedes: "))
        status = input("Status (Ativa, Finalizada, Cancelada): ")

       
        df_hospede = oracle.sqlToDataFrame(f"SELECT * FROM hospede WHERE cpf = '{cpf}'")
        if df_hospede.empty:
            print(f"O hóspede com CPF {cpf} não existe.")
            return None
        hospede = Hospede(
            df_hospede.cpf.values[0],
            df_hospede.nome.values[0],
            df_hospede.telefone.values[0],
            str(df_hospede.data_cadastro.values[0])
        )

        df_quarto = oracle.sqlToDataFrame(f"SELECT * FROM quarto WHERE numero_quarto = {numero_quarto}")
        if df_quarto.empty:
            print(f"O quarto {numero_quarto} não existe.")
            return None
        quarto = Quarto(
            df_quarto.numero_quarto.values[0],
            df_quarto.tipo.values[0],
            df_quarto.valor_diaria.values[0],
            df_quarto.status.values[0]
        )

        
        checkin = datetime.strptime(data_checkin, "%Y-%m-%d")
        checkout = datetime.strptime(data_checkout, "%Y-%m-%d")
        dias = (checkout - checkin).days
        if dias <= 0:
            print("A data de check-out deve ser posterior à data de check-in.")
            return None

        valor_total = dias * quarto.get_valor_diaria()

        oracle.write(f"""
            INSERT INTO reserva (
                id_reserva, cpf, numero_quarto, data_checkin, data_checkout,
                qtd_hospedes, valor_total, status, criado_em
            ) VALUES (
                reserva_seq.NEXTVAL,
                '{cpf}', {numero_quarto},
                TO_DATE('{data_checkin}', 'YYYY-MM-DD'),
                TO_DATE('{data_checkout}', 'YYYY-MM-DD'),
                {qtd_hospedes}, {valor_total}, '{status}', SYSTIMESTAMP
            )
        """)

        df_reserva = oracle.sqlToDataFrame("""
            SELECT * FROM (
                SELECT * FROM reserva ORDER BY id_reserva DESC
            ) WHERE ROWNUM = 1
        """)

        nova_reserva = Reserva(
            df_reserva.id_reserva.values[0],
            hospede,
            quarto,
            str(df_reserva.data_checkin.values[0]),
            str(df_reserva.data_checkout.values[0]),
            df_reserva.qtd_hospedes.values[0],
            df_reserva.valor_total.values[0],
            df_reserva.status.values[0],
            str(df_reserva.criado_em.values[0])
        )

        print("\nReserva criada com sucesso!")
        print(nova_reserva.to_string())
        return nova_reserva

    def verifica_existencia_reserva(self, oracle: OracleQueries, id_reserva: int) -> bool:
        df = oracle.sqlToDataFrame(f"SELECT id_reserva FROM reserva WHERE id_reserva = {id_reserva}")
        return not df.empty

    
    def atualizar_reserva_interactive(self) -> Reserva:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df = oracle.sqlToDataFrame("SELECT id_reserva, cpf, numero_quarto, data_checkin, data_checkout, status FROM reserva ORDER BY id_reserva")
        if df.empty:
            print("Nenhuma reserva cadastrada.")
            return None

        for i, row in enumerate(df.itertuples(), start=1):
            print(f"{i}) ID: {row.id_reserva} - CPF: {row.cpf} - Quarto: {row.numero_quarto} - {row.status}")

        escolha = input("Selecione o número da tupla que deseja atualizar: ")
        try:
            idx = int(escolha) - 1
            id_reserva = int(df.id_reserva.values[idx])
        except Exception:
            print("Seleção inválida")
            return None

        escolha_attr = input("Atualizar todos os atributos? (S para sim / N para escolher um): ").strip().upper()
        if escolha_attr == 'S':
            data_checkin = input("Data de check-in (YYYY-MM-DD): ")
            data_checkout = input("Data de check-out (YYYY-MM-DD): ")
            qtd_hospedes = int(input("Quantidade de hóspedes: "))
            status = input("Status (Ativa, Finalizada, Cancelada): ")
            oracle.write(f"""
                UPDATE reserva
                SET data_checkin = TO_DATE('{data_checkin}', 'YYYY-MM-DD'), data_checkout = TO_DATE('{data_checkout}', 'YYYY-MM-DD'), qtd_hospedes = {qtd_hospedes}, status = '{status}'
                WHERE id_reserva = {id_reserva}
            """)
        else:
            print("Escolha o atributo:\n1) data_checkin\n2) data_checkout\n3) qtd_hospedes\n4) status")
            opt = input("Opção: ")
            if opt == '1':
                data_checkin = input("Data de check-in (YYYY-MM-DD): ")
                oracle.write(f"UPDATE reserva SET data_checkin = TO_DATE('{data_checkin}', 'YYYY-MM-DD') WHERE id_reserva = {id_reserva}")
            elif opt == '2':
                data_checkout = input("Data de check-out (YYYY-MM-DD): ")
                oracle.write(f"UPDATE reserva SET data_checkout = TO_DATE('{data_checkout}', 'YYYY-MM-DD') WHERE id_reserva = {id_reserva}")
            elif opt == '3':
                qtd_hospedes = int(input("Quantidade de hóspedes: "))
                oracle.write(f"UPDATE reserva SET qtd_hospedes = {qtd_hospedes} WHERE id_reserva = {id_reserva}")
            elif opt == '4':
                status = input("Status (Ativa, Finalizada, Cancelada): ")
                oracle.write(f"UPDATE reserva SET status = '{status}' WHERE id_reserva = {id_reserva}")
            else:
                print("Opção inválida")
                return None

        df_reserva = oracle.sqlToDataFrame(f"SELECT * FROM reserva WHERE id_reserva = {id_reserva}")
        
        df_hospede = oracle.sqlToDataFrame(f"SELECT * FROM hospede WHERE cpf = '{df_reserva.cpf.values[0]}'")
        hospede = Hospede(df_hospede.cpf.values[0], df_hospede.nome.values[0], df_hospede.telefone.values[0], str(df_hospede.data_cadastro.values[0]))
        df_quarto = oracle.sqlToDataFrame(f"SELECT * FROM quarto WHERE numero_quarto = {df_reserva.numero_quarto.values[0]}")
        quarto = Quarto(df_quarto.numero_quarto.values[0], df_quarto.tipo.values[0], df_quarto.valor_diaria.values[0], df_quarto.status.values[0])

        reserva_atualizada = Reserva(
            df_reserva.id_reserva.values[0],
            hospede,
            quarto,
            str(df_reserva.data_checkin.values[0]),
            str(df_reserva.data_checkout.values[0]),
            df_reserva.qtd_hospedes.values[0],
            df_reserva.valor_total.values[0],
            df_reserva.status.values[0],
            str(df_reserva.criado_em.values[0])
        )
        print("\nReserva atualizada com sucesso!\n")
        print(reserva_atualizada.to_string())
        return reserva_atualizada

    
    def excluir_reserva_interactive(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df = oracle.sqlToDataFrame("SELECT id_reserva, cpf, numero_quarto, status FROM reserva ORDER BY id_reserva")
        if df.empty:
            print("Nenhuma reserva cadastrada.")
            return

        for i, row in enumerate(df.itertuples(), start=1):
            print(f"{i}) ID: {row.id_reserva} - CPF: {row.cpf} - Quarto: {row.numero_quarto} - {row.status}")

        escolha = input("Selecione o número da tupla que deseja excluir: ")
        try:
            idx = int(escolha) - 1
            id_reserva = int(df.id_reserva.values[idx])
        except Exception:
            print("Seleção inválida")
            return

        resp = input(f"Confirma exclusão da reserva {id_reserva}? (S/N): ").strip().upper()
        if resp != 'S':
            print("Operação cancelada. Voltando ao menu.")
            return

        df_reserva = oracle.sqlToDataFrame(f"SELECT * FROM reserva WHERE id_reserva = {id_reserva}")
        oracle.write(f"DELETE FROM reserva WHERE id_reserva = {id_reserva}")

        hospede = Hospede(df_reserva.cpf.values[0], None, None, None) if not df_reserva.empty else None
        quarto = Quarto(df_reserva.numero_quarto.values[0], None, None, None) if not df_reserva.empty else None
        reserva_excluida = Reserva(
            df_reserva.id_reserva.values[0],
            hospede,
            quarto,
            str(df_reserva.data_checkin.values[0]),
            str(df_reserva.data_checkout.values[0]),
            df_reserva.qtd_hospedes.values[0],
            df_reserva.valor_total.values[0],
            df_reserva.status.values[0],
            str(df_reserva.criado_em.values[0])
        )
        print("\nReserva removida com sucesso!\n")
        print(reserva_excluida.to_string())