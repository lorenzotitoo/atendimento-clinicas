from Model.abstractPagamento import AbstractPagamento

class Dinheiro(AbstractPagamento):
    def modalidade(self) -> str:
        return "Dinheiro"

    def detalhar_pagamento(self) -> dict:
        return {"modalidade": self.modalidade(),
                "cpf": self.paciente.cpf,
                "valor_pago": self.valor_pago}