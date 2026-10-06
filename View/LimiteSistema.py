class LimiteSistema:
    def limite_opcoes(self) -> int:
        print("\n===== SISTEMA DA CLÍNICA =====")
        print("1 - Clínicas")
        print("2 - Pacientes")
        print("3 - Profissionais")
        print("4 - Atendimentos")
        print("5 - Relatórios")
        print("0 - Sair")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1
 
    def limite_mensagem(self, mensagem: str):
        print(mensagem)
 