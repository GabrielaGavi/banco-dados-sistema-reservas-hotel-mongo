class Quarto:
    def __init__(self, numero_quarto: int=None, tipo: str=None, valor_diaria: float=None, status: str=None):
        self.set_numero_quarto(numero_quarto)
        self.set_tipo(tipo)
        self.set_valor_diaria(valor_diaria)
        self.set_status(status)

    
    def get_numero_quarto(self) -> int:
        return self.__numero_quarto

    def get_tipo(self) -> str:
        return self.__tipo

    def get_valor_diaria(self) -> float:
        return self.__valor_diaria

    def get_status(self) -> str:
        return self.__status

    
    def set_numero_quarto(self, numero_quarto: int):
        self.__numero_quarto = numero_quarto

    def set_tipo(self, tipo: str):
        self.__tipo = tipo

    def set_valor_diaria(self, valor_diaria: float):
        self.__valor_diaria = valor_diaria

    def set_status(self, status: str):
        self.__status = status

    
    def to_string(self) -> str:
        return f"{self.__numero_quarto} - {self.__tipo} - R${self.__valor_diaria:.2f} - {self.__status}"
