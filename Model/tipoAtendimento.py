from enum import Enum

class TipoAtendimento(Enum):
    CONSULTA = 1
    EXAME = 2
    RETORNO = 3
    PROCEDIMENTO = 4
    EMERGENCIA = 5