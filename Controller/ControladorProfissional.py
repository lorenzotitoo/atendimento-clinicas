from Model.profissionalDeSaude import ProfissionalDeSaude
from Model.excecoes import SistemaClinicaError
from Model.validacoes import validar_cpf
from View.LimiteProfissional import LimiteProfissional

class ControladorProfissional:
    def __init__(self, controlador_sistema: "ControladorSistema"):
        self.__controlador_sistema = controlador_sistema
        self.__profissionais = []
        self.__limite_profissional = LimiteProfissional()

    @property
    def profissionais(self) -> list[ProfissionalDeSaude]:
        return self.__profissionais

    @property
    def limite_profissional(self) -> LimiteProfissional:
        return self.__limite_profissional


    def incluir_profissional(self):
        dados = self.__limite_profissional.coletar_dados_profissional()
        if dados is None:
            return
        if self.buscar_profissional(dados["cpf"]) is not None:
            self.__limite_profissional.limite_mensagem("Já existe um profissional com esse CPF.")
            return
        try:
            profissional = ProfissionalDeSaude(dados["nome"],
                                           dados["celular"],
                                           dados["cpf"],
                                           dados["especialidade"],
                                           dados["registro_profissional"])
            self.__profissionais.append(profissional)
            self.__limite_profissional.limite_mensagem("Profissional incluído com sucesso.")

        except SistemaClinicaError as erro:
            self.__limite_profissional.limite_mensagem(f"Ocorreu um erro ao tentar cadastrar o Profissional: {erro}")

    def listar_profissionais(self):
        self.__limite_profissional.exibir_profissionais(self.__profissionais)
    
    def alterar_profissional(self):
        profissional = self.buscar_profissional(self.__limite_profissional.escolher_profissional())
        if profissional is None:
            self.__limite_profissional.limite_mensagem("Profissional não encontrado.")
            return
        dados = self.__limite_profissional.coletar_dados_profissional()
        if dados is None:
            return
        if dados["cpf"] != profissional.cpf and self.buscar_profissional(dados["cpf"]) is not None:
            self.__limite_profissional.limite_mensagem("Já existe um profissional com esse CPF.")
            return
            
        try:
            validar_cpf(dados["cpf"])
        except SistemaClinicaError as erro:
            self.__limite_profissional.limite_mensagem(str(erro))
            return
            
        profissional.nome = dados["nome"]
        profissional.celular = dados["celular"]
        profissional.cpf = dados["cpf"]
        profissional.especialidade = dados["especialidade"]
        profissional.registro_profissional = dados["registro_profissional"]
        self.__limite_profissional.limite_mensagem("Profissional alterado com sucesso.")

    def excluir_profissional(self):
        profissional = self.buscar_profissional(self.__limite_profissional.escolher_profissional())
        if profissional is None:
            self.__limite_profissional.limite_mensagem("Profissional não encontrado.")
            return
            
        for atendimento in self.__controlador_sistema.controlador_atendimentos.atendimentos:
            em_uso = atendimento.profissional is profissional
            for procedimento in atendimento.procedimentos:
                if procedimento.profissional is profissional:
                    em_uso = True
            if em_uso:
                self.__limite_profissional.limite_mensagem(
                    "Não é possível excluir: o profissional possui atendimentos ou procedimentos cadastrados.")
                return
        # remove o vínculo com as clínicas antes de excluir
        for clinica in self.__controlador_sistema.controlador_clinicas.clinicas:
            if profissional in clinica.profissionais:
                clinica.excluir_profissional(profissional)
        self.__profissionais.remove(profissional)
        self.__limite_profissional.limite_mensagem("Profissional excluído com sucesso.")

    def buscar_profissional(self, cpf: str) -> ProfissionalDeSaude:
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        return None

    def abre_menu(self):
            opcoes = {
                1: self.incluir_profissional,
                2: self.listar_profissionais,
                3: self.alterar_profissional,
                4: self.excluir_profissional,
            }

            while True:
                opcao = self.__limite_profissional.limite_opcoes()
                

                if opcao == 0:
                    break
                funcao_escolhida = opcoes.get(opcao)
                
                if funcao_escolhida:
                    funcao_escolhida()
        
                else:
                    self.__limite_profissional.limite_mensagem("Opção inválida! Digite um número válido.")