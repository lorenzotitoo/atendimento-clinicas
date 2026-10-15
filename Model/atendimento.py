from decimal import Decimal
from datetime import date as Date, time as Time
from Model.clinica import Clinica
from Model.paciente import Paciente
from Model.profissionalDeSaude import ProfissionalDeSaude
from Model.tipoAtendimento import TipoAtendimento
from Model.procedimento import Procedimento
from Model.abstractPagamento import AbstractPagamento
from Model.excecoes import (HorarioInvalidoError,
                            ForaDoHorarioError,
                            ProfissionalNaoVinculadoError,
                            PacienteMenorDeIdadeError,
                            PagamentoAposDataError,
                            ValorInvalidoError)
from Model.validacoes import IDADE_MINIMA_ATENDIMENTO

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
        self.__pagamentos = []
        self.__procedimentos = []
        self.__validar(clinica, paciente, profissional, data, horario_inicio, horario_fim, valor_total)
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__data = data
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo_atendimento = tipo_atendimento
        self.__valor_total = valor_total
        self.__id_atendimento = None
        

    def __validar(self, clinica, paciente, profissional, data, horario_inicio, horario_fim, valor_total):
        if horario_fim <= horario_inicio:
            raise HorarioInvalidoError("O horário de fim deve ser maior que o de início.")
        if horario_inicio < clinica.horario_fun_inicio or horario_fim > clinica.horario_fun_fim:
            raise ForaDoHorarioError(
            f"O atendimento está fora do horário de funcionamento da clínica. "
            f"Funcionamento: {clinica.horario_fun_inicio.strftime('%H:%M')} às "
            f"{clinica.horario_fun_fim.strftime('%H:%M')}."
            )
        if profissional not in clinica.profissionais:
            raise ProfissionalNaoVinculadoError("Profissional não está vinculado a esta clínica.")
        for procedimento in self.__procedimentos:
            if procedimento.profissional not in clinica.profissionais:
                raise ProfissionalNaoVinculadoError(
                "Existe procedimento neste atendimento com profissional não vinculado à clínica informada."
            )
        if paciente.idade_em(data) < IDADE_MINIMA_ATENDIMENTO:
            raise PacienteMenorDeIdadeError(
                f"O paciente precisa ter pelo menos {IDADE_MINIMA_ATENDIMENTO} anos completos na data do atendimento."
            )
        total_pago = sum(p.valor_pago for p in self.__pagamentos)
        for pagamento in self.__pagamentos:
            if pagamento.data > data:
                raise PagamentoAposDataError("Existem pagamentos com data posterior à data informada para o atendimento.")
        if valor_total < total_pago:
            raise ValorInvalidoError(f"O valor total não pode ser menor que o valor já pago (R$ {total_pago:.2f}).")
    
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

    def alterar_dados(self, clinica, paciente, profissional, data, horario_inicio, horario_fim, tipo_atendimento, valor_total):
        self.__validar(clinica, paciente, profissional, data, horario_inicio, horario_fim, valor_total)
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__data = data
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__tipo_atendimento = tipo_atendimento
        self.__valor_total = valor_total
        
        # Atualiza o paciente nos pagamentos existentes
        for pagamento in self.__pagamentos:
            pagamento.paciente = paciente
    
    def adicionar_procedimento(self, procedimento: Procedimento):
        if not isinstance(procedimento, Procedimento):
            raise TypeError("O objeto informado não é um procedimento válido.")
        if procedimento in self.__procedimentos:
            raise ValueError("Este procedimento já foi incluído no atendimento.")
        if procedimento.profissional not in self.__clinica.profissionais:
            raise ProfissionalNaoVinculadoError("O profissional do procedimento não está vinculado à clínica do atendimento.")
        self.__procedimentos.append(procedimento)

    def alterar_procedimento(self, procedimento: Procedimento, descricao: str, custo: Decimal, profissional: ProfissionalDeSaude):
        if not isinstance(procedimento, Procedimento):
            raise TypeError("O objeto informado não é um procedimento válido.")
        if procedimento not in self.__procedimentos:
            raise ValueError("Este procedimento não está associado ao atendimento.")
        if profissional not in self.__clinica.profissionais:
            raise ProfissionalNaoVinculadoError("O profissional do procedimento não está vinculado à clínica do atendimento.")
        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.profissional = profissional
    
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
        if pagamento.data > self.__data:
            raise PagamentoAposDataError("O pagamento deve ser realizado até a data do atendimento.")
        if pagamento.valor_pago <= 0 or pagamento.valor_pago > self.calcular_valor_restante():
            raise ValorInvalidoError("O valor pago deve ser maior que zero e não pode ultrapassar o valor restante.")
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
