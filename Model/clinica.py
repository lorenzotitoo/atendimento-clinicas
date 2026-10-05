from datetime import time as Time

class Clinica:
    def __init__(self,
                nome: str, 
                cidade: str, 
                descricao: str, 
                horario_fun_inicio: Time,
                horario_fun_fim: Time):
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__horario_fun_inicio = horario_fun_inicio
        self.__horario_fun_fim = horario_fun_fim
        self.__profissionais = []

    @property
    def nome(self):
        return self.__nome                      
    @nome.setter
    def nome(self, nome):   
        self.__nome = nome  

    @property
    def cidade(self):
        return self.__cidade
    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade

    @property
    def descricao(self):
        return self.__descricao 
    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    @property
    def horario_fun_inicio(self):
        return self.__horario_fun_inicio    
    @horario_fun_inicio.setter
    def horario_fun_inicio(self, horario_fun_inicio):   
        self.__horario_fun_inicio = horario_fun_inicio

    @property
    def horario_fun_fim(self):      
        return self.__horario_fun_fim
    @horario_fun_fim.setter
    def horario_fun_fim(self, horario_fun_fim):
        self.__horario_fun_fim = horario_fun_fim

    @property
    def profissionais(self):
        return self.__profissionais

    def adicionar_profissional(self, profissional):
        if profissional in self.__profissionais:
            raise ValueError(
                "Profissional já vinculado a esta clínica."
            )

        self.__profissionais.append(profissional)
    