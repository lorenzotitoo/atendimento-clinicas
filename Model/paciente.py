from Model.abstractPessoa import AbstractPessoa
from datetime import date as Date

class Paciente(AbstractPessoa):
    def __init__(self,
        nome: str,
        celular: str,
        cpf: str,
        data_nasc: Date):
        super().__init__(nome, celular, cpf)
        self.__data_nasc = data_nasc
    @property
    def data_nasc(self) -> Date:
        return self.__data_nasc
    @data_nasc.setter
    def data_nasc(self, data_nasc: Date):
        self.__data_nasc = data_nasc

    @property
    def idade(self) -> int:
        hoje = Date.today()
        idade = hoje.year - self.__data_nasc.year
        if (hoje.month, hoje.day) < (self.__data_nasc.month, self.__data_nasc.day):
            idade -= 1
        return idade

    def tipo_pessoa(self) -> str:
        return "Paciente"