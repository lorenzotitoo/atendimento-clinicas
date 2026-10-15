from View.entrada import ler_campo, OperacaoCanceladaError

class LimiteProfissional:
    def limite_opcoes(self) -> int:
        print("\n===== PROFISSIONAIS =====")
        print("1 - Incluir profissional")
        print("2 - Listar profissionais")
        print("3 - Alterar profissional")
        print("4 - Excluir profissional")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def coletar_dados_profissional(self) -> dict:
        print("(Digite 0 em qualquer campo para cancelar)")
        
        try:
            # Uso do ler_campo() garante que se digitar "0", o fluxo pula direto para o except OperacaoCanceladaError
            nome = ler_campo("Nome: ")
            celular = ler_campo("Celular: ")
            cpf = ler_campo("CPF: ")
            especialidade = ler_campo("Especialidade: ")
            registro_profissional = ler_campo("Registro profissional: ")
            if not nome or not celular or not cpf or not especialidade or not registro_profissional:
                self.limite_mensagem("Existe(m) campo(s) obrigatório(s) vazio(s)")
                return None
        except OperacaoCanceladaError:
            self.limite_mensagem("Operação cancelada.")
            return None
        
        return {"nome": nome,
                "celular": celular,
                "cpf": cpf,
                "especialidade": especialidade,
                "registro_profissional": registro_profissional}

    def escolher_profissional(self) -> str:
        return input("CPF do profissional: ").strip()

    def exibir_profissionais(self, profissionais):
        if len(profissionais) == 0:
            print("Nenhum profissional cadastrado.")
            return
        for profissional in profissionais:
            print("-" * 30)
            print(f"Nome: {profissional.nome}")
            print(f"Celular: {profissional.celular}")
            print(f"CPF: {profissional.cpf}")
            print(f"Especialidade: {profissional.especialidade}")
            print(f"Registro profissional: {profissional.registro_profissional}")

    def limite_mensagem(self, mensagem: str):
        print(mensagem)