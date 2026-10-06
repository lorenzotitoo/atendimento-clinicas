from Controller.ControladorClinica import ControladorClinica
from Controller.ControladorPaciente import ControladorPaciente
from Controller.ControladorProfissional import ControladorProfissional
from Controller.ControladorAtendimento import ControladorAtendimento
from Controller.ControladorRelatorio import ControladorRelatorio
from View.LimiteSistema import LimiteSistema

class ControladorSistema:
    def __init__(self):
        self.__limite_sistema = LimiteSistema()
        
        self.__controlador_clinicas = ControladorClinica(self)
        self.__controlador_pacientes = ControladorPaciente(self)
        self.__controlador_profissionais = ControladorProfissional(self)
        self.__controlador_atendimentos = ControladorAtendimento(self)
        self.__controlador_relatorios = ControladorRelatorio(self)

    @property
    def limite_sistema(self) -> LimiteSistema:
        return self.__limite_sistema
    
    @property
    def controlador_clinicas(self) -> ControladorClinica:
        return self.__controlador_clinicas
 
    @property
    def controlador_pacientes(self) -> ControladorPaciente:
        return self.__controlador_pacientes
 
    @property
    def controlador_profissionais(self) -> ControladorProfissional:
        return self.__controlador_profissionais
 
    @property
    def controlador_atendimentos(self):
        return self.__controlador_atendimentos
 
    @property
    def controlador_relatorios(self):
        return self.__controlador_relatorios

    def abre_menu(self):
        opcoes = {
            1: self.cadastrar_clinicas,
            2: self.cadastrar_pacientes,
            3: self.cadastrar_profissionais,
            4: self.gerenciar_atendimentos,
            5: self.gerar_relatorios,
            0: self.encerrar_sistema
        }

        while True:
            opcao = self.__limite_sistema.limite_opcoes()
            
            if opcao == -1 or opcao == 0:
                self.encerrar_sistema()
                break
                
            funcao_escolhida = opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
            else:
                self.__limite_sistema.limite_mensagem("Opção inválida! Digite um número do menu.")

    def cadastrar_clinicas(self):
        self.__controlador_clinicas.abre_menu()

    def cadastrar_pacientes(self):
        self.__controlador_pacientes.abre_menu()

    def cadastrar_profissionais(self):
        self.__controlador_profissionais.abre_menu()

    def gerenciar_atendimentos(self):
        self.__controlador_atendimentos.abre_menu()

    def gerar_relatorios(self):
        self.__controlador_relatorios.abre_menu()

    def encerrar_sistema(self):
        self.__limite_sistema.limite_mensagem("Encerrando o Sistema de Clínicas... Até logo!")