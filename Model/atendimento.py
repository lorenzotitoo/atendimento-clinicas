from decimal import Decimal
from datetime import date as Date, time as Time
from Model.clinica import Clinica
from Model.paciente import Paciente
from Model.profissionalDeSaude import ProfissionalDeSaude
from Model.tipoAtendimento import TipoAtendimento
from Model.procedimento import Procedimento
from Model.abstractPagamento import AbstractPagamento

class Atendimento:
    def __init__(self,
                clinica: Clinica,
                paciente: Paciente,
                profissional: ProfissionalDeSaude,
                data: Date,
                horario_inicio: Time,
                horario_fim: Time,
                tipo_atendimento: TipoAtendimento,
                valor_total: Decimal):
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__data = data
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo_atendimento = tipo_atendimento
        self.__valor_total = valor_total
        self.__id_atendimento = None
        self.__pagamentos = []
        self.__procedimentos = []

    @property
    def clinica(self) -> Clinica:
        return self.__clinica
    @clinica.setter
    def clinica(self, clinica: Clinica):
        self.__clinica = clinica

    @property
    def paciente(self) -> Paciente:
        return self.__paciente
    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = paciente

    @property
    def profissional(self) -> ProfissionalDeSaude:
        return self.__profissional
    @profissional.setter
    def profissional(self, profissional: ProfissionalDeSaude):
        self.__profissional = profissional

    @property
    def data(self) -> Date:
        return self.__data
    @data.setter
    def data(self, data: Date):
        self.__data = data

    @property
    def horario_inicio(self) -> Time:
        return self.__horario_inicio
    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: Time):
        self.__horario_inicio = horario_inicio

    @property
    def horario_fim(self) -> Time:
        return self.__horario_fim
    @horario_fim.setter
    def horario_fim(self, horario_fim: Time):
        self.__horario_fim = horario_fim

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento
    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: TipoAtendimento):
        self.__tipo_atendimento = tipo_atendimento

    @property
    def valor_total(self) -> Decimal:
        return self.__valor_total
    @valor_total.setter
    def valor_total(self, valor_total: Decimal):
        self.__valor_total = valor_total

    @property
    def id_atendimento(self) -> int:
        return self.__id_atendimento
    @id_atendimento.setter
    def id_atendimento(self, id_atendimento: int):
        self.__id_atendimento = id_atendimento

    @property
    def procedimentos(self) -> Procedimento:
        return self.__procedimentos

    def adicionar_procedimento(self, procedimento: Procedimento):
        if not isinstance(procedimento, Procedimento):
            raise TypeError("O objeto informado não é um procedimento válido.")
        if procedimento in self.__procedimentos:
            raise ValueError("Este procedimento já foi incluído no atendimento.")
        self.__procedimentos.append(procedimento)

    def remover_procedimento(self, procedimento: Procedimento):
        if not isinstance(procedimento, Procedimento):
            raise TypeError("O objeto informado não é um procedimento válido.")
        if procedimento not in self.__procedimentos:
            raise ValueError("Este procedimento não está associado ao atendimento.")
        self.__procedimentos.remove(procedimento)

    @property
    def pagamentos(self) -> list[AbstractPagamento]:
        return self.__pagamentos

    def adicionar_pagamento(self, pagamento: AbstractPagamento):
        if not isinstance(pagamento, AbstractPagamento):
            raise TypeError("O objeto informado não é um pagamento válido.")
        if pagamento in self.__pagamentos:
            raise ValueError("Este pagamento já foi incluído no atendimento.")
        self.__pagamentos.append(pagamento)

    def remover_pagamento(self, pagamento: AbstractPagamento):
        if not isinstance(pagamento, AbstractPagamento):
            raise TypeError("O objeto informado não é um pagamento válido.")
        if pagamento not in self.__pagamentos:
            raise ValueError("Este pagamento não está associado ao atendimento.")
        self.__pagamentos.remove(pagamento)

    def calcular_valor_restante(self) -> Decimal:
        valores_pagos = []
        for pagamento in self.__pagamentos:
            valores_pagos.append(pagamento.valor_pago)
        total_pago = sum(valores_pagos)
        return self.__valor_total - total_pago
