from datetime import date as Date, time as Time
from Model.excecoes import (CpfInvalidoError,
                            DataNascimentoInvalidaError,
                            CartaoInvalidoError,
                            HorarioInvalidoError)
# Constante de negócio para maioridade no atendimento
IDADE_MINIMA_ATENDIMENTO = 18

def validar_cpf(cpf: str):
    """Valida o formato e os dois dígitos verificadores do CPF de acordo com o algoritmo oficial."""
    if not isinstance(cpf, str) or len(cpf) != 11 or not (cpf.isascii() and cpf.isdigit()):
        raise CpfInvalidoError("CPF inválido. Informe exatamente 11 dígitos, somente números.")
    if cpf == cpf[0] * 11:
        raise CpfInvalidoError("CPF inválido. Sequências de dígitos repetidos não são permitidas.")
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = soma_1 % 11
    digito_1 = 0 if resto_1 < 2 else 11 - resto_1

    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = soma_2 % 11
    digito_2 = 0 if resto_2 < 2 else 11 - resto_2

    if int(cpf[9]) != digito_1 or int(cpf[10]) != digito_2:
        raise CpfInvalidoError("CPF inválido. Os dígitos verificadores não conferem.")

def validar_data_nascimento(data_nasc: Date):
    if data_nasc > Date.today():
        raise DataNascimentoInvalidaError("A data de nascimento não pode ser uma data futura.")
    
    if Date.today().year - data_nasc.year > 130:
        raise DataNascimentoInvalidaError("A data de nascimento informada é irrealista.")

def validar_numero_cartao(num_cartao: str):
    """Valida o número do cartão de crédito através do Algoritmo de Luhn (módulo 10)."""
    if not isinstance(num_cartao, str) or not (num_cartao.isascii() and num_cartao.isdigit()) or not 13 <= len(num_cartao) <= 19:
        raise CartaoInvalidoError("Número de cartão inválido. Informe de 13 a 19 dígitos, somente números.")

    soma = 0
    inverter = False
    for digito in reversed(num_cartao):
        n = int(digito)
        if inverter:
            n *= 2
            if n > 9:
                n -= 9
        soma += n
        inverter = not inverter

    if soma % 10 != 0:
        raise CartaoInvalidoError("Número de cartão inválido.")

def validar_horario_funcionamento(horario_inicio: Time, horario_fim: Time):
    if horario_fim <= horario_inicio:
        raise HorarioInvalidoError("O horário de fechamento deve ser maior que o de abertura.")

def calcular_idade(data_nasc: Date, data_referencia: Date) -> int:
    idade = data_referencia.year - data_nasc.year
    if (data_referencia.month, data_referencia.day) < (data_nasc.month, data_nasc.day):
        idade -= 1
    return idade