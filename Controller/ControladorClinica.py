from Model.clinica import Clinica
from Model.excecoes import SistemaClinicaError
from Model.validacoes import validar_horario_funcionamento
from View.LimiteClinica import LimiteClinica

class ControladorClinica:
    def __init__(self, controlador_sistema: "ControladorSistema"):
        self.__clinicas = []
        self.__controlador_sistema = controlador_sistema
        self.__limite_clinica = LimiteClinica()

    @property
    def clinicas(self) -> list[Clinica]:
        return self.__clinicas
 
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
 
    @property
    def limite_clinica(self) -> LimiteClinica:
        return self.__limite_clinica

    def incluir_clinica(self):
        dados = self.__limite_clinica.coletar_dados_clinica()
        if dados is None:
            return
        if self.buscar_clinica(dados["nome"]) is not None:
            self.__limite_clinica.limite_mensagem("Já existe uma clínica com esse nome.")
            return
        try:
            clinica = Clinica(dados["nome"],
                            dados["cidade"],
                            dados["descricao"],
                            dados["horario_fun_inicio"],
                            dados["horario_fun_fim"])
            self.__clinicas.append(clinica)
            self.__limite_clinica.limite_mensagem("Clínica incluída com sucesso.")
        except SistemaClinicaError as erro:
            self.__limite_clinica.limite_mensagem(f"Ocorreu um erro ao tentar cadastrar a clínica: {erro}")

    def listar_clinicas(self):
        self.__limite_clinica.exibir_clinicas(self.__clinicas)

    def alterar_clinica(self):
        clinica = self.buscar_clinica(self.__limite_clinica.escolher_clinica())
        if clinica is None:
            self.__limite_clinica.limite_mensagem("Clínica não encontrada.")
            return
        dados = self.__limite_clinica.coletar_dados_clinica()
        if dados is None:
            return
        if dados["nome"].lower() != clinica.nome.lower() and self.buscar_clinica(dados["nome"]) is not None:
            self.__limite_clinica.limite_mensagem("Já existe uma clínica com esse nome.")
            return
        
        try:
            validar_horario_funcionamento(dados["horario_fun_inicio"], dados["horario_fun_fim"])
        except SistemaClinicaError as erro:
            self.__limite_clinica.limite_mensagem(str(erro))
            return

        for atendimento in self.__controlador_sistema.controlador_atendimentos.atendimentos:
            if atendimento.clinica is clinica:
                if (atendimento.horario_inicio < dados["horario_fun_inicio"]
                        or atendimento.horario_fim > dados["horario_fun_fim"]):
                    self.__limite_clinica.limite_mensagem(
                        "Não é possível alterar: existem atendimentos desta clínica fora do novo horário de funcionamento.")
                    return

        clinica.nome = dados["nome"]
        clinica.cidade = dados["cidade"]
        clinica.descricao = dados["descricao"]
        clinica.horario_fun_inicio = dados["horario_fun_inicio"]
        clinica.horario_fun_fim = dados["horario_fun_fim"]
        self.__limite_clinica.limite_mensagem("Clínica alterada com sucesso.")

    def excluir_clinica(self):
        clinica = self.buscar_clinica(self.__limite_clinica.escolher_clinica())
        if clinica is None:
            self.__limite_clinica.limite_mensagem("Clínica não encontrada.")
            return
        
        for atendimento in self.__controlador_sistema.controlador_atendimentos.atendimentos:
            if atendimento.clinica is clinica:
                self.__limite_clinica.limite_mensagem("Não é possível excluir: a clínica possui atendimentos cadastrados.")
                return
                
        self.__clinicas.remove(clinica)
        self.__limite_clinica.limite_mensagem("Clínica excluída com sucesso.")
    
    def buscar_clinica(self, nome: str) -> Clinica:
        for clinica in self.__clinicas:
            if clinica.nome.lower() == nome.lower():
                return clinica
        return None   

    def vincular_profissional(self):
        clinica = self.buscar_clinica(self.__limite_clinica.escolher_clinica())
        if clinica is None:
            self.__limite_clinica.limite_mensagem("Clínica não encontrada.")
            return
        controlador_profissionais = self.__controlador_sistema.controlador_profissionais
        cpf = controlador_profissionais.limite_profissional.escolher_profissional()
        profissional = controlador_profissionais.buscar_profissional(cpf)
        if profissional is None:
            self.__limite_clinica.limite_mensagem("Profissional não encontrado.")
            return
        
        try:
            clinica.adicionar_profissional(profissional)
            self.__limite_clinica.limite_mensagem(
                "Profissional vinculado com sucesso."
            )
        except ValueError as erro:
            self.__limite_clinica.limite_mensagem(str(erro))
    
    def remover_profissional(self):
        clinica = self.buscar_clinica(self.__limite_clinica.escolher_clinica())
        if clinica is None:
            self.__limite_clinica.limite_mensagem("Clínica não encontrada.")
            return
        controlador_profissionais = self.__controlador_sistema.controlador_profissionais
        cpf = controlador_profissionais.limite_profissional.escolher_profissional()
        profissional = controlador_profissionais.buscar_profissional(cpf)
        if profissional is None:
            self.__limite_clinica.limite_mensagem("Profissional não encontrado")
            return
            
        for atendimento in self.__controlador_sistema.controlador_atendimentos.atendimentos:
            if atendimento.clinica is clinica:
                em_uso = atendimento.profissional is profissional
                for procedimento in atendimento.procedimentos:
                    if procedimento.profissional is profissional:
                        em_uso = True
                if em_uso:
                    self.__limite_clinica.limite_mensagem(
                        "Não é possível desvincular: o profissional possui atendimentos ou procedimentos nesta clínica.")
                    return
                    
        try:
            clinica.excluir_profissional(profissional)
            self.__limite_clinica.limite_mensagem(
                "Profissional desvinculado com sucesso."
            )
        except ValueError as erro:
            self.__limite_clinica.limite_mensagem(str(erro))

    def abre_menu(self):
        opcoes = {
            1: self.incluir_clinica,
            2: self.listar_clinicas,
            3: self.alterar_clinica,
            4: self.excluir_clinica,
            5: self.vincular_profissional,
            6: self.remover_profissional,
        }

        while True:
            opcao = self.__limite_clinica.limite_opcoes()

            
            if opcao == 0:
                break
            
            funcao_escolhida = opcoes.get(opcao)
            
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__limite_clinica.limite_mensagem("Opção inválida! Digite um número válido.")
