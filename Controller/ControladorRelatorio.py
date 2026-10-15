from View.LimiteRelatorio import LimiteRelatorio
 
class ControladorRelatorio:
    def __init__(self, controlador_sistema: "ControladorSistema"):
        self.__controlador_sistema = controlador_sistema
        self.__limite_relatorio = LimiteRelatorio()

    @property
    def limite_relatorio(self) -> LimiteRelatorio:
        return self.__limite_relatorio

    def gerar_relatorio_clinicas_com_mais_atendimentos(self):
        atendimentos = self.__controlador_sistema.controlador_atendimentos.atendimentos
        clinicas_atendimentos = []
        for clinica in self.__controlador_sistema.controlador_clinicas.clinicas:
            quantidade = 0
            for atendimento in atendimentos:
                if atendimento.clinica is clinica:
                    quantidade += 1
            clinicas_atendimentos.append((clinica, quantidade))
        
        # Ordena em ordem decrescente de quantidade
        clinicas_atendimentos.sort(key=lambda item: item[1], reverse=True)
        self.__limite_relatorio.exibir_clinicas_atendimentos(clinicas_atendimentos)

    def gerar_relatorio_atendimentos_caros_baratos(self):
        atendimentos = list(self.__controlador_sistema.controlador_atendimentos.atendimentos)
        atendimentos.sort(key=lambda atendimento: atendimento.valor_total, reverse=True)
        self.__limite_relatorio.exibir_atendimentos_valores(atendimentos)

    def gerar_relatorio_procedimentos_mais_realizados(self):
        contagem = {}
        for atendimento in self.__controlador_sistema.controlador_atendimentos.atendimentos:
            for procedimento in atendimento.procedimentos:
                chave = procedimento.descricao.strip().lower()
                if chave in contagem:
                    contagem[chave][1] += 1
                else:
                    contagem[chave] = [procedimento.descricao.strip(), 1]
        procedimentos_realizados = [(descricao, quantidade) for descricao, quantidade in contagem.values()]
        procedimentos_realizados.sort(key=lambda item: item[1], reverse=True)
        self.__limite_relatorio.exibir_procedimentos_realizados(procedimentos_realizados)

    def gerar_relatorio_procedimentos_caros_baratos(self):
        procedimentos = []
        for atendimento in self.__controlador_sistema.controlador_atendimentos.atendimentos:
            for procedimento in atendimento.procedimentos:
                procedimentos.append(procedimento)
        procedimentos.sort(key=lambda procedimento: procedimento.custo, reverse=True)
        self.__limite_relatorio.exibir_procedimentos_valores(procedimentos)

    def abre_menu(self):
        opcoes = {
            1: self.gerar_relatorio_clinicas_com_mais_atendimentos,
            2: self.gerar_relatorio_atendimentos_caros_baratos,
            3: self.gerar_relatorio_procedimentos_mais_realizados,
            4: self.gerar_relatorio_procedimentos_caros_baratos,
        }
    
        while True:
            opcao = self.__limite_relatorio.limite_opcoes()
            
    
            if opcao == 0:
                break
            funcao_escolhida = opcoes.get(opcao)
                    
            if funcao_escolhida:
                funcao_escolhida()
            
            else:
                self.__limite_relatorio.limite_mensagem("Opção inválida! Digite um número válido.")

    