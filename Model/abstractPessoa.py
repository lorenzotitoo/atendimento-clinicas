from abc import ABC, abstractmethod
from Model.validacoes import validar_cpf

class AbstractPessoa(ABC):
    def __init__(self, nome: str, celular: str, cpf: str):
        self.__nome = nome
        self.__celular = celular
        validar_cpf(cpf)
        self.__cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome
    @nome.setter
    def nome(self, nome: str):
        self.__nome = nome

    @property
    def celular(self) -> str:
        return self.__celular
    @celular.setter
    def celular(self, celular: str):
        self.__celular = celular

    @property
    def cpf(self) -> str:
        return self.__cpf
    @cpf.setter
    def cpf(self, cpf: str):
        validar_cpf(cpf)
        self.__cpf = cpf

    # Método abstrato que deve ser implementado pelas subclasses
    @abstractmethod
    def tipo_pessoa(self) -> str:
        pass

