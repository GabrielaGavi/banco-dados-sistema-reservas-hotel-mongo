from model.hospede import Hospede
from model.quarto import Quarto

class Reserva:
    def __init__(
        self,
        id_reserva: int = None,
        hospede: Hospede = None,
        quarto: Quarto = None,
        data_checkin: str = None,
        data_checkout: str = None,
        qtd_hospedes: int = None,
        valor_total: float = None,
        status: str = None,
        criado_em: str = None
    ):
        self.set_id_reserva(id_reserva)
        self.set_hospede(hospede)
        self.set_quarto(quarto)
        self.set_data_checkin(data_checkin)
        self.set_data_checkout(data_checkout)
        self.set_qtd_hospedes(qtd_hospedes)
        self.set_valor_total(valor_total)
        self.set_status(status)
        self.set_criado_em(criado_em)

    
    def get_id_reserva(self) -> int:
        return self.__id_reserva

    def get_hospede(self) -> Hospede:
        return self.__hospede

    def get_quarto(self) -> Quarto:
        return self.__quarto

    def get_data_checkin(self) -> str:
        return self.__data_checkin

    def get_data_checkout(self) -> str:
        return self.__data_checkout

    def get_qtd_hospedes(self) -> int:
        return self.__qtd_hospedes

    def get_valor_total(self) -> float:
        return self.__valor_total

    def get_status(self) -> str:
        return self.__status

    def get_criado_em(self) -> str:
        return self.__criado_em

    
    def set_id_reserva(self, id_reserva: int):
        self.__id_reserva = id_reserva

    def set_hospede(self, hospede: Hospede):
        self.__hospede = hospede

    def set_quarto(self, quarto: Quarto):
        self.__quarto = quarto

    def set_data_checkin(self, data_checkin: str):
        self.__data_checkin = data_checkin

    def set_data_checkout(self, data_checkout: str):
        self.__data_checkout = data_checkout

    def set_qtd_hospedes(self, qtd_hospedes: int):
        self.__qtd_hospedes = qtd_hospedes

    def set_valor_total(self, valor_total: float):
        self.__valor_total = valor_total

    def set_status(self, status: str):
        self.__status = status

    def set_criado_em(self, criado_em: str):
        self.__criado_em = criado_em

    
    def to_string(self) -> str:
        return (
            f"Reserva {self.__id_reserva} - "
            f"Hóspede: {self.__hospede.get_nome()} ({self.__hospede.get_cpf()}) - "
            f"Quarto: {self.__quarto.get_numero_quarto()} ({self.__quarto.get_tipo()}) - "
            f"Check-in: {self.__data_checkin} - Check-out: {self.__data_checkout} - "
            f"Hóspedes: {self.__qtd_hospedes} - Total: R${self.__valor_total:.2f} - "
            f"Status: {self.__status} - Criada em: {self.__criado_em}"
        )
