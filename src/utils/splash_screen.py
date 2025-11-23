from conexion.mongo_queries import MongoQueries


class SplashScreen:

    def __init__(self):

        self.qry_total_hospedes = "mongo_count_hospede"
        self.qry_total_quartos  = "mongo_count_quarto"
        self.qry_total_reservas = "mongo_count_reserva"

        self.created_by = "Davi Pereira de Sousa, Gabriela Gave Gavi, José Luiz dos Santos Azeredo, Pedro Henrique Bispo, Pedro Henrique Ferreira Bonela"
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

        self.mongo = MongoQueries(database="hotel_reservas")

    def get_total_hospedes(self):
        self.mongo.connect()
        total = self.mongo.db["hospede"].count_documents({})
        self.mongo.close()
        return total

    def get_total_quartos(self):
        self.mongo.connect()
        total = self.mongo.db["quarto"].count_documents({})
        self.mongo.close()
        return total

    def get_total_reservas(self):
        self.mongo.connect()
        total = self.mongo.db["reserva"].count_documents({})
        self.mongo.close()
        return total

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

    def show(self):
        print(self.get_updated_screen())
