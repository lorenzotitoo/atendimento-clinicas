from Model.clinica import Clinica
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
        except Exception as e:
            self.__limite_clinica.limite_mensagem(f"Ocorreu um erro ao tentar cadastrar a clínica: {e}")

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
        self.__clinicas.remove(clinica)
        self.__limite_clinica.limite_mensagem("Clínica excluída com sucesso.")
    
    def buscar_clinica(self, nome: str) -> Clinica:
        for clinica in self.__clinicas:
            if clinica.nome == nome:
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
            
            if opcao == -1:
                self.__controlador_sistema.encerrar_sistema()
                break
            if opcao == 0:
                break
            
            funcao_escolhida = opcoes.get(opcao)
            
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__limite_clinica.limite_mensagem("Opção inválida! Digite um número válido.")
