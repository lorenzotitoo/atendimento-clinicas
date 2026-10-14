from datetime import date as Date
from decimal import Decimal
from Model.abstractPagamento import AbstractPagamento
from Model.atendimento import Atendimento
from Model.paciente import Paciente
from Model.validacoes import validar_numero_cartao

class CartaoCredito(AbstractPagamento):
    def __init__(self,
        data: Date,
        atendimento: Atendimento,
        paciente: Paciente,
        valor_pago: Decimal,
        num_cartao: str,
        bandeira: str):
        super().__init__(data, atendimento, paciente, valor_pago)
        self.__num_cartao = num_cartao
        self.__bandeira = bandeira

    @property
    def num_cartao(self) -> str:
        return self.__num_cartao
    @num_cartao.setter
    def num_cartao(self, num_cartao: str):
        validar_numero_cartao(num_cartao)
        self.__num_cartao = num_cartao

    @property
    def bandeira(self) -> str:
        return self.__bandeira
    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = bandeira

    def modalidade(self) -> str:
        return "Cartão de Crédito"

    def detalhar_pagamento(self) -> dict:
        return {"modalidade": self.modalidade(),
                "bandeira": self.__bandeira,
                "valor_pago": self.valor_pago}