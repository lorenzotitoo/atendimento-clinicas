from enum import Enum

class TipoAtendimento(Enum):
    # Enumeração que define os tipos estáticos de agendamentos possíveis na clínica.
    CONSULTA = 1
    EXAME = 2
    RETORNO = 3
    PROCEDIMENTO = 4
    EMERGENCIA = 5