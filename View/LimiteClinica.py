from datetime import datetime
from View.entrada import ler_campo, OperacaoCanceladaError

class LimiteClinica:
    def limite_opcoes(self) -> int:
        print("\n===== CLÍNICAS =====")
        print("1 - Incluir clínica")
        print("2 - Listar clínicas")
        print("3 - Alterar clínica")
        print("4 - Excluir clínica")
        print("5 - Vincular profissional")
        print("6 - Remover profissional")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def coletar_dados_clinica(self) -> dict:
        print("(Digite 0 em qualquer campo para cancelar)")
        try:
            # Uso do ler_campo() garante que se digitar "0", o fluxo pula direto para o except OperacaoCanceladaError
            nome = ler_campo("Nome: ")
            cidade = ler_campo("Cidade: ")
            descricao = ler_campo("Descrição: ")
            horario_fun_inicio = datetime.strptime(ler_campo("Horário de abertura (HH:MM): "), "%H:%M").time()
            horario_fun_fim = datetime.strptime(ler_campo("Horário de fechamento (HH:MM): "), "%H:%M").time()
            
            if not nome or not cidade or not descricao:
                self.limite_mensagem("Existe(m) campo(s) obrigatório(s) vazio(s)")
                return None
                
        except OperacaoCanceladaError:
            self.limite_mensagem("Operação cancelada.")
            return None
        except ValueError:
            self.limite_mensagem("Horário inválido. Use o formato HH:MM.")
            return None

        return {"nome": nome,
                "cidade": cidade,
                "descricao": descricao,
                "horario_fun_inicio": horario_fun_inicio,
                "horario_fun_fim": horario_fun_fim}

    def escolher_clinica(self) -> str:
        return input("Nome da clínica: ").strip()

    def exibir_clinicas(self, clinicas):
        if len(clinicas) == 0:
            print("Nenhuma clínica cadastrada.")
            return
        for clinica in clinicas:
            print("-" * 30)
            print(f"Nome: {clinica.nome}")
            print(f"Cidade: {clinica.cidade}")
            print(f"Descrição: {clinica.descricao}")
            print(f"Funcionamento: {clinica.horario_fun_inicio.strftime('%H:%M')} às {clinica.horario_fun_fim.strftime('%H:%M')}")
            print("Profissionais:")
            if len(clinica.profissionais) == 0:
                print("  Nenhum profissional vinculado.")
            for profissional in clinica.profissionais:
                print(f"  {profissional.nome} - {profissional.especialidade} ({profissional.registro_profissional})")

    def limite_mensagem(self, mensagem: str):
        print(mensagem)