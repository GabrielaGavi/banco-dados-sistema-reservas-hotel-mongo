from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        
        self.qry_total_hospedes = config.QUERY_COUNT.format(tabela="hospede")
        self.qry_total_quartos = config.QUERY_COUNT.format(tabela="quarto")
        self.qry_total_reservas = config.QUERY_COUNT.format(tabela="reserva")
        

        
        self.created_by = "Davi Pereira de Sousa, Gabriela Gave Gavi, José Luiz dos Santos Azeredo, Pedro Henrique Bispo, Pedro Henrique Ferreira Bonela"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

    def get_total_hospedes(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_hospedes)["total_hospede"].values[0]

    def get_total_quartos(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_quartos)["total_quarto"].values[0]

    def get_total_reservas(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_reservas)["total_reserva"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #            SISTEMA DE RESERVAS DE HOTEL              
        #                                                     
        #  TOTAL DE REGISTROS:                                
        #      1 - HÓSPEDES:      {str(self.get_total_hospedes()).rjust(5)}
        #      2 - QUARTOS:       {str(self.get_total_quartos()).rjust(5)}
        #      3 - RESERVAS:      {str(self.get_total_reservas()).rjust(5)}
        #
        #  CRIADO POR:  {self.created_by}
        #
        #  PROFESSOR:   {self.professor}
        #
        #  DISCIPLINA:  {self.disciplina}
        #               {self.semestre}
        ########################################################
        """

