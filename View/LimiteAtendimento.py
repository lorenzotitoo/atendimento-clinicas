from datetime import datetime
from decimal import Decimal, InvalidOperation
from Model.atendimento import Atendimento
from Model.procedimento import Procedimento
from Model.abstractPagamento import AbstractPagamento
from Model.tipoAtendimento import TipoAtendimento

class LimiteAtendimento:
    def limite_opcoes(self) -> int:
        print("\n===== ATENDIMENTOS =====")
        print("1 - Incluir atendimento")
        print("2 - Listar atendimentos")
        print("3 - Alterar atendimento")
        print("4 - Excluir atendimento")
        print("5 - Incluir procedimento")
        print("6 - Listar procedimentos")
        print("7 - Excluir procedimento")
        print("8 - Incluir pagamento")
        print("9 - Excluir pagamento")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def coletar_dados_atendimento(self) -> dict:
        try:
            cpf_paciente = input("CPF do paciente: ").strip()
            nome_clinica = input("Nome da clínica: ").strip()
            cpf_profissional = input("CPF do profissional: ").strip()

            if not cpf_paciente or not nome_clinica or not cpf_profissional:
                self.limite_mensagem(
                    "Existe(m) campo(s) obrigatório(s) vazio(s)"
                )
                return None

            data = datetime.strptime(input("Data (DD/MM/AAAA): "), "%d/%m/%Y").date()
            horario_inicio = datetime.strptime(input("Horário de início (HH:MM): "), "%H:%M").time()
            horario_fim = datetime.strptime(input("Horário de fim (HH:MM): "), "%H:%M").time()
            for tipo in TipoAtendimento:
                print(f"{tipo.value} - {tipo.name}")
            tipo_atendimento = TipoAtendimento(int(input("Tipo de atendimento: ")))
            valor_total = Decimal(input("Valor total: ").replace(",", "."))
            if not valor_total.is_finite() or valor_total <= 0:
                raise ValueError
        except (ValueError, InvalidOperation):
            self.limite_mensagem("Dados inválidos. Verifique data (DD/MM/AAAA), horários (HH:MM), tipo e valor.")
            return None
        return {"cpf_paciente": cpf_paciente,
                "nome_clinica": nome_clinica,
                "cpf_profissional": cpf_profissional,
                "data": data,
                "horario_inicio": horario_inicio,
                "horario_fim": horario_fim,
                "tipo_atendimento": tipo_atendimento,
                "valor_total": valor_total}

    def escolher_atendimento(self) -> int:
        try:
            return int(input("ID do atendimento: "))
        except ValueError:
            return None

    def exibir_atendimentos(self, atendimentos: list[Atendimento]):
        if len(atendimentos) == 0:
            print("Nenhum atendimento cadastrado.")
            return
        for atendimento in atendimentos:
            print("-" * 30)
            print(f"ID: {atendimento.id_atendimento}")
            print(f"Clínica: {atendimento.clinica.nome}")
            print(f"Paciente: {atendimento.paciente.nome}")
            print(f"Profissional: {atendimento.profissional.nome}")
            print(f"Data: {atendimento.data.strftime('%d/%m/%Y')}")
            print(f"Horário: {atendimento.horario_inicio.strftime('%H:%M')} às {atendimento.horario_fim.strftime('%H:%M')}")
            print(f"Tipo: {atendimento.tipo_atendimento.name}")
            print(f"Valor total: R$ {atendimento.valor_total:.2f}")
            print(f"Procedimentos: {len(atendimento.procedimentos)}")
            print(f"Pagamentos: {len(atendimento.pagamentos)}")

    def coletar_dados_procedimento(self) -> dict:
        try:
            descricao = input("Descrição: ").strip()
            custo = Decimal(input("Custo: ").replace(",", "."))
            cpf_profissional = input("CPF do profissional: ").strip()
        except InvalidOperation:
            self.limite_mensagem("Custo inválido.")
            return None

        if not custo.is_finite() or custo <= 0:
            self.limite_mensagem("Custo inválido. Informe um valor maior que zero.")
            return None

        if not descricao or not cpf_profissional:
            self.limite_mensagem("Existe(m) campo(s) obrigatório(s) vazio(s)")
            return None

        return {"descricao": descricao,
                "custo": custo,
                "cpf_profissional": cpf_profissional}

    def escolher_procedimento(self) -> int:
        try:
            return int(input("Número do procedimento: "))
        except ValueError:
            return 0

    def exibir_procedimentos(self, procedimentos: list[Procedimento]):
        if len(procedimentos) == 0:
            print("Nenhum procedimento cadastrado.")
            return
        for i, procedimento in enumerate(procedimentos, start=1):
            print(f"{i} - {procedimento.descricao} | R$ {procedimento.custo:.2f} | {procedimento.profissional.nome}")

    def coletar_dados_pagamento(self) -> dict:
        try:
            print("1 - Dinheiro")
            print("2 - Pix")
            print("3 - Cartão de Crédito")
            modalidade = int(input("Modalidade: "))
            if modalidade not in (1, 2, 3):
                raise ValueError
            data = datetime.strptime(input("Data do pagamento (DD/MM/AAAA): "), "%d/%m/%Y").date()
            valor_pago = Decimal(input("Valor pago: ").replace(",", "."))
            dados = {"modalidade": modalidade,
                     "data": data,
                     "valor_pago": valor_pago}
            if modalidade == 2:
                dados["cpf_pagador"] = input("CPF do pagador: ").strip()
            elif modalidade == 3:
                dados["num_cartao"] = input("Número do cartão: ").strip()
                dados["bandeira"] = input("Bandeira: ").strip()
        except (ValueError, InvalidOperation):
            self.limite_mensagem("Dados inválidos. Verifique modalidade, data (DD/MM/AAAA) e valor.")
            return None
        return dados

    def escolher_pagamento(self) -> int:
        try:
            return int(input("Número do pagamento: "))
        except ValueError:
            return 0

    def exibir_pagamentos(self, pagamentos: list[AbstractPagamento]):
        if len(pagamentos) == 0:
            print("Nenhum pagamento cadastrado.")
            return
        for i, pagamento in enumerate(pagamentos, start=1):
            detalhes = pagamento.detalhar_pagamento()
            texto = " | ".join(f"{chave}: {valor}" for chave, valor in detalhes.items())
            print(f"{i} - {pagamento.data.strftime('%d/%m/%Y')} | {texto}")

    def exibir_valor_restante(self, valor_restante: Decimal):
        print(f"Valor restante: R$ {valor_restante:.2f}")
 
    def limite_mensagem(self, mensagem: str):
        print(mensagem)

    
    