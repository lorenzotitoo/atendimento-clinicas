# Exceção para interromper fluxos de cadastro ou alteração quando o usuário decidir 
class OperacaoCanceladaError(Exception):
    pass

# Função auxiliar que substitui o input() padrão do sistema.
def ler_campo(texto: str) -> str:
    valor = input(texto).strip()
    if valor == "0":
        raise OperacaoCanceladaError
    return valor