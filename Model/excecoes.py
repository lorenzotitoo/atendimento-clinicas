class SistemaClinicaError(Exception):
    pass

class CpfInvalidoError(SistemaClinicaError):
    pass

class DataNascimentoInvalidaError(SistemaClinicaError):
    pass

class CartaoInvalidoError(SistemaClinicaError):
    pass

class HorarioInvalidoError(SistemaClinicaError):
    pass

class ForaDoHorarioError(SistemaClinicaError):
    pass

class PacienteMenorDeIdadeError(SistemaClinicaError):
    pass

class ProfissionalNaoVinculadoError(SistemaClinicaError):
    pass

class PagamentoAposDataError(SistemaClinicaError):
    pass

class ValorInvalidoError(SistemaClinicaError):
    pass