from Model.abstractPessoa import AbstractPessoa

class ProfissionalDeSaude(AbstractPessoa):
    def __init__(self,
        nome: str,
        celular: str,
        cpf: str,
        especialidade: str,
        registro_profissional: str):
        super().__init__(nome, celular, cpf)
        self.__especialidade = especialidade
        self.__registro_profissional = registro_profissional

    @property
    def especialidade(self) -> str:
        return self.__especialidade
    @especialidade.setter
    def especialidade(self, especialidade: str):
        self.__especialidade = especialidade

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional
    @registro_profissional.setter
    def registro_profissional(self, registro_profissional: str):
        self.__registro_profissional = registro_profissional

    def tipo_pessoa(self) -> str:
        return "Profissional de Saúde"