class Hospede:
    def __init__(self, cpf: str = None, nome: str = None, telefone: str = None, data_cadastro: str = None):
        self.set_cpf(cpf)
        self.set_nome(nome)
        self.set_telefone(telefone)
        self.set_data_cadastro(data_cadastro)

    
    def get_cpf(self) -> str:
        return self.__cpf

    def get_nome(self) -> str:
        return self.__nome

    def get_telefone(self) -> str:
        return self.__telefone

    def get_data_cadastro(self) -> str:
        return self.__data_cadastro

    
    def set_cpf(self, cpf: str) -> None:
        self.__cpf = cpf

    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def set_telefone(self, telefone: str) -> None:
        self.__telefone = telefone

    def set_data_cadastro(self, data_cadastro: str) -> None:
        self.__data_cadastro = data_cadastro
        
    def formatar_cpf(self):
        cpf = str(self.__cpf).zfill(11)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    
    def to_string(self) -> str:
        return f"{self.formatar_cpf()} - {self.__nome} - {self.__telefone} - {self.__data_cadastro}"
