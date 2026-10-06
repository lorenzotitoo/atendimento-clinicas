from datetime import datetime

class LimitePaciente:
    def limite_opcoes(self) -> int:
        print("\n===== PACIENTES =====")
        print("1 - Incluir paciente")
        print("2 - Listar pacientes")
        print("3 - Alterar paciente")
        print("4 - Excluir paciente")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def coletar_dados_paciente(self) -> dict:
        try:
            nome = input("Nome: ").strip()
            celular = input("Celular: ").strip()
            cpf = input("CPF: ").strip()
            data_nasc = datetime.strptime(input("Data de nascimento (DD/MM/AAAA): "), "%d/%m/%Y").date()
            if not nome or not celular or not cpf:
                self.limite_mensagem("Existe(m) campo(s) obrigatório(s) vazio(s)")
                return None
        except ValueError:
            self.limite_mensagem("Data inválida. Use o formato DD/MM/AAAA.")
            return None
        return {"nome": nome,
                "celular": celular,
                "cpf": cpf,
                "data_nasc": data_nasc}

    def escolher_paciente(self) -> str:
        return input("CPF do paciente: ").strip()

    def exibir_pacientes(self, pacientes):
        if len(pacientes) == 0:
            print("Nenhum paciente cadastrado.")
            return
        for paciente in pacientes:
            print("-" * 30)
            print(f"Nome: {paciente.nome}")
            print(f"Celular: {paciente.celular}")
            print(f"CPF: {paciente.cpf}")
            print(f"Data de nascimento: {paciente.data_nasc.strftime('%d/%m/%Y')} ({paciente.idade} anos)")

    def limite_mensagem(self, mensagem: str):
        print(mensagem)

    