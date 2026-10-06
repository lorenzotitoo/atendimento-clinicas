from Model.clinica import Clinica
from Model.atendimento import Atendimento
from Model.procedimento import Procedimento

class LimiteRelatorio:
    def limite_opcoes(self) -> int:
        print("\n===== RELATÓRIOS =====")
        print("1 - Clínicas com mais atendimentos")
        print("2 - Atendimentos mais caros e mais baratos")
        print("3 - Procedimentos mais realizados")
        print("4 - Procedimentos mais caros e mais baratos")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def exibir_clinicas_atendimentos(self, clinicas_atendimentos: list[tuple[Clinica, int]]):
        print("\n--- Clínicas com mais atendimentos ---")
        if len(clinicas_atendimentos) == 0:
            print("Nenhuma clínica cadastrada.")
            return
        for i, (clinica, quantidade) in enumerate(clinicas_atendimentos, start=1):
            print(f"{i}. {clinica.nome} - {quantidade} atendimento(s)")

    def exibir_atendimentos_valores(self, atendimentos: list[Atendimento]):
        print("\n--- Atendimentos do mais caro ao mais barato ---")
        if len(atendimentos) == 0:
            print("Nenhum atendimento cadastrado.")
            return
        for i, atendimento in enumerate(atendimentos, start=1):
            print(f"{i}. ID {atendimento.id_atendimento} | {atendimento.paciente.nome} | "
                  f"{atendimento.clinica.nome} | {atendimento.data.strftime('%d/%m/%Y')} | "
                  f"R$ {atendimento.valor_total:.2f}")

    def exibir_procedimentos_valores(self, procedimentos: list[Procedimento]):
        print("\n--- Procedimentos do mais caro ao mais barato ---")
        if len(procedimentos) == 0:
            print("Nenhum procedimento cadastrado.")
            return
        for i, procedimento in enumerate(procedimentos, start=1):
            print(f"{i}. {procedimento.descricao} | R$ {procedimento.custo:.2f} | {procedimento.profissional.nome}")

    def exibir_procedimentos_realizados(self, procedimentos_realizados: list[tuple[str, int]]):
        print("\n--- Procedimentos mais realizados ---")
        if len(procedimentos_realizados) == 0:
            print("Nenhum procedimento cadastrado.")
            return
        for i, (descricao, quantidade) in enumerate(procedimentos_realizados, start=1):
            print(f"{i}. {descricao} - {quantidade} vez(es)")

    def limite_mensagem(self, mensagem: str):
            print(mensagem)