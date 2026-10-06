from Model.atendimento import Atendimento
from Model.procedimento import Procedimento
from Model.dinheiro import Dinheiro
from Model.pix import Pix
from Model.cartaoCredito import CartaoCredito
from View.LimiteAtendimento import LimiteAtendimento

class ControladorAtendimento:
    def __init__(self, controlador_sistema: "ControladorSistema"):
        self.__atendimentos = []
        self.__controlador_sistema = controlador_sistema
        self.__limite_atendimento = LimiteAtendimento()

    @property
    def atendimentos(self) -> list[Atendimento]:
        return self.__atendimentos

    @property
    def limite_atendimento(self) -> LimiteAtendimento:
        return self.__limite_atendimento

    def __buscar_referencias(self, dados: dict) -> tuple:
        # retorna (paciente, clinica, profissional) ou None se algo for inválido
        paciente = self.__controlador_sistema.controlador_pacientes.buscar_paciente(dados["cpf_paciente"])
        if paciente is None:
            self.__limite_atendimento.limite_mensagem("Paciente não encontrado.")
            return None
        clinica = self.__controlador_sistema.controlador_clinicas.buscar_clinica(dados["nome_clinica"])
        if clinica is None:
            self.__limite_atendimento.limite_mensagem("Clínica não encontrada.")
            return None
        profissional = self.__controlador_sistema.controlador_profissionais.buscar_profissional(dados["cpf_profissional"])
        if profissional is None:
            self.__limite_atendimento.limite_mensagem("Profissional não encontrado.")
            return None
        if profissional not in clinica.profissionais:
            self.__limite_atendimento.limite_mensagem("Profissional não está vinculado a esta clínica.")
            return None
        if dados["horario_fim"] <= dados["horario_inicio"]:
            self.__limite_atendimento.limite_mensagem("O horário de fim deve ser maior que o de início.")
            return None

        if (
        dados["horario_inicio"] < clinica.horario_fun_inicio
        or
        dados["horario_fim"] > clinica.horario_fun_fim
        ):
            self.__limite_atendimento.limite_mensagem(
            f"O atendimento está fora do horário de funcionamento da clínica. "
            f"Funcionamento: "
            f"{clinica.horario_fun_inicio.strftime('%H:%M')} às "
            f"{clinica.horario_fun_fim.strftime('%H:%M')}."
        )
            return None
        return paciente, clinica, profissional

    def incluir_atendimento(self):
        dados = self.__limite_atendimento.coletar_dados_atendimento()
        if dados is None:
            return
        referencias = self.__buscar_referencias(dados)
        if referencias is None:
            return
        paciente, clinica, profissional = referencias
        atendimento = Atendimento(clinica,
                                  paciente,
                                  profissional,
                                  dados["data"],
                                  dados["horario_inicio"],
                                  dados["horario_fim"],
                                  dados["tipo_atendimento"],
                                  dados["valor_total"])
        atendimento.id_atendimento = max([a.id_atendimento for a in self.__atendimentos], default=0) + 1
        self.__atendimentos.append(atendimento)
        self.__limite_atendimento.limite_mensagem(f"Atendimento incluído com sucesso. ID: {atendimento.id_atendimento}")

    def listar_atendimentos(self):
        self.__limite_atendimento.exibir_atendimentos(self.__atendimentos)

    def alterar_atendimento(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        dados = self.__limite_atendimento.coletar_dados_atendimento()
        if dados is None:
            return
        referencias = self.__buscar_referencias(dados)
        if referencias is None:
            return
        paciente, clinica, profissional = referencias
        atendimento.paciente = paciente
        atendimento.clinica = clinica
        atendimento.profissional = profissional
        atendimento.data = dados["data"]
        atendimento.horario_inicio = dados["horario_inicio"]
        atendimento.horario_fim = dados["horario_fim"]
        atendimento.tipo_atendimento = dados["tipo_atendimento"]
        atendimento.valor_total = dados["valor_total"]
        self.__limite_atendimento.limite_mensagem("Atendimento alterado com sucesso.")

    def excluir_atendimento(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        self.__atendimentos.remove(atendimento)
        self.__limite_atendimento.limite_mensagem("Atendimento excluído com sucesso.")

    def buscar_atendimento(self, id_atendimento: int) -> Atendimento:
        for atendimento in self.__atendimentos:
            if atendimento.id_atendimento == id_atendimento:
                return atendimento
        return None

    def incluir_procedimento(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        dados = self.__limite_atendimento.coletar_dados_procedimento()
        if dados is None:
            return
        profissional = self.__controlador_sistema.controlador_profissionais.buscar_profissional(dados["cpf_profissional"])
        if profissional is None:
            self.__limite_atendimento.limite_mensagem("Profissional não encontrado.")
            return
        procedimento = Procedimento(dados["descricao"], dados["custo"], profissional)
        if atendimento.adicionar_procedimento(procedimento):
            self.__limite_atendimento.limite_mensagem("Procedimento incluído com sucesso.")
        else:
            self.__limite_atendimento.limite_mensagem("Não foi possível incluir o procedimento.")

    def excluir_procedimento(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        self.__limite_atendimento.exibir_procedimentos(atendimento.procedimentos)
        indice = self.__limite_atendimento.escolher_procedimento()
        if indice < 1 or indice > len(atendimento.procedimentos):
            self.__limite_atendimento.limite_mensagem("Procedimento não encontrado.")
            return
        try:
            atendimento.remover_procedimento(atendimento.procedimentos[indice - 1])
            self.__limite_atendimento.limite_mensagem("Procedimento excluído com sucesso.")
        except Exception as erro:
            self.__limite_atendimento.limite_mensagem(f"Ocorreu um erro ao tentar excluir o Procedimento: {erro}")


    def listar_procedimentos(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        self.__limite_atendimento.exibir_procedimentos(atendimento.procedimentos)

    def incluir_pagamento(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        valor_restante = atendimento.calcular_valor_restante()
        self.__limite_atendimento.exibir_valor_restante(valor_restante)
        if valor_restante <= 0:
            self.__limite_atendimento.limite_mensagem("Este atendimento já está quitado.")
            return
        dados = self.__limite_atendimento.coletar_dados_pagamento()
        if dados is None:
            return
        if dados["valor_pago"] <= 0 or dados["valor_pago"] > valor_restante:
            self.__limite_atendimento.limite_mensagem("O valor pago deve ser maior que zero e não pode ultrapassar o valor restante.")
            return
        if dados["modalidade"] == 1:
            pagamento = Dinheiro(dados["data"], atendimento, atendimento.paciente, dados["valor_pago"])
        elif dados["modalidade"] == 2:
            pagamento = Pix(dados["data"], atendimento, atendimento.paciente, dados["valor_pago"], dados["cpf_pagador"])
        else:
            pagamento = CartaoCredito(dados["data"], atendimento, atendimento.paciente, dados["valor_pago"],
                                      dados["num_cartao"], dados["bandeira"])
        if atendimento.adicionar_pagamento(pagamento):
            self.__limite_atendimento.limite_mensagem("Pagamento incluído com sucesso.")
            self.__limite_atendimento.exibir_valor_restante(atendimento.calcular_valor_restante())
        else:
            self.__limite_atendimento.limite_mensagem("Não foi possível incluir o pagamento.")

    def excluir_pagamento(self):
        atendimento = self.buscar_atendimento(self.__limite_atendimento.escolher_atendimento())
        if atendimento is None:
            self.__limite_atendimento.limite_mensagem("Atendimento não encontrado.")
            return
        self.__limite_atendimento.exibir_pagamentos(atendimento.pagamentos)
        indice = self.__limite_atendimento.escolher_pagamento()
        if indice < 1 or indice > len(atendimento.pagamentos):
            self.__limite_atendimento.limite_mensagem("Pagamento não encontrado.")
            return
        try:
            atendimento.remover_pagamento(atendimento.pagamentos[indice - 1])
            self.__limite_atendimento.limite_mensagem("Pagamento excluído com sucesso.")
            self.__limite_atendimento.exibir_valor_restante(atendimento.calcular_valor_restante())
        except Exception as erro:
            self.__limite_atendimento.limite_mensagem(f"Ocorreu um erro ao tentar excluir o Pagamento: {erro}")

    def abre_menu(self):
            opcoes = {
                1: self.incluir_atendimento,
                2: self.listar_atendimentos,
                3: self.alterar_atendimento,
                4: self.excluir_atendimento,
                5: self.incluir_procedimento,
                6: self.listar_procedimentos,
                7: self.excluir_procedimento,
                8: self.incluir_pagamento,
                9: self.excluir_pagamento
            }
    
            while True:
                opcao = self.__limite_atendimento.limite_opcoes()
                
    
                if opcao == 0:
                    break
                funcao_escolhida = opcoes.get(opcao)
                
                if funcao_escolhida:
                    funcao_escolhida()
        
                else:
                    self.__limite_atendimento.limite_mensagem("Opção inválida! Digite um número válido.")

    

    