from conexion.oracle_queries import OracleQueries
from utils.config import clear_console

class Relatorios:
    def __init__(self):
        
        clear_console()
        
        self.oracle = OracleQueries()

    def executar_relatorio(self, caminho_sql: str):
        
        self.oracle.connect()

        
        with open(caminho_sql, "r") as f:
            query = f.read()

        
        df = self.oracle.sqlToDataFrame(query)

        if df.empty:
            print("\n### Nenhum dado encontrado para este relatório. ###\n")
        else:
            print(df.to_string(index=False))

        
        self.oracle.close()

        input("\nPressione Enter para voltar ao menu...\n")
        return df

    def relatorio_reservas_por_status(self):
        print("\n### RELATÓRIO DE RESERVAS POR STATUS ###")
        return self.executar_relatorio("src/sql/relatorio_reservas_por_status.sql")

    def relatorio_reservas_detalhado(self):
        print("\n### RELATÓRIO DE RESERVAS DETALHADO ###")
        return self.executar_relatorio("src/sql/relatorio_reservas_detalhado.sql")

    def relatorio_reservas_por_mes(self):
        print("\n### RELATÓRIO DE RESERVAS POR MÊS ###")
        return self.executar_relatorio("src/sql/relatorio_reservas_por_mes.sql")

    def relatorio_hospedes(self):
        print("\n### RELATÓRIO DE HÓSPEDES ###")
        return self.executar_relatorio("src/sql/relatorio_hospedes.sql")
