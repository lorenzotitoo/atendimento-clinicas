from datetime import date as Date
from decimal import Decimal
from Model.abstractPagamento import AbstractPagamento
from Model.atendimento import Atendimento
from Model.paciente import Paciente

class Pix(AbstractPagamento):
    def __init__(self,
        data: Date,
        atendimento: Atendimento,
        paciente: Paciente,
        valor_pago: Decimal,
        cpf_pagador: str):
        super().__init__(data, atendimento, paciente, valor_pago)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador
    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        self.__cpf_pagador = cpf_pagador

    def modalidade(self) -> str:
        return "Pix"

    def detalhar_pagamento(self) -> dict:
        return {"modalidade": self.modalidade(),
                "cpf_pagador": self.__cpf_pagador,
                "valor_pago": self.valor_pago}