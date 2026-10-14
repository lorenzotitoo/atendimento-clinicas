from Model.abstractPessoa import AbstractPessoa
from Model.validacoes import validar_data_nascimento, calcular_idade
from datetime import date as Date

class Paciente(AbstractPessoa):
    def __init__(self,
        nome: str,
        celular: str,
        cpf: str,
        data_nasc: Date):
        super().__init__(nome, celular, cpf)
        validar_data_nascimento(data_nasc)
        self.__data_nasc = data_nasc
    @property
    def data_nasc(self) -> Date:
        return self.__data_nasc
    @data_nasc.setter
    def data_nasc(self, data_nasc: Date):
        validar_data_nascimento(data_nasc)
        self.__data_nasc = data_nasc

    @property
    def idade(self) -> int:
        return calcular_idade(self.__data_nasc, Date.today())

    def idade_em(self, data: Date) -> int:
        return calcular_idade(self.__data_nasc, data)

    def tipo_pessoa(self) -> str:
        return "Paciente"