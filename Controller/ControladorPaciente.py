from Model.paciente import Paciente
from View.LimitePaciente import LimitePaciente

class ControladorPaciente:
    def __init__(self, controlador_sistema: "ControladorSistema"):
        self.__controlador_sistema = controlador_sistema
        self.__pacientes = []
        self.__limite_paciente = LimitePaciente()

    @property
    def pacientes(self) -> list[Paciente]:
        return self.__pacientes

    @property
    def limite_paciente(self) -> LimitePaciente:
        return self.__limite_paciente

    def incluir_paciente(self):
        dados = self.__limite_paciente.coletar_dados_paciente()
        if dados is None:
            return
        if self.buscar_paciente(dados["cpf"]) is not None:
            self.__limite_paciente.limite_mensagem("Já existe um paciente com esse CPF.")
            return
        try:
            paciente = Paciente(
                dados["nome"],
                dados["celular"],
                dados["cpf"],
                dados["data_nasc"]
            )
            self.__pacientes.append(paciente)
            self.__limite_paciente.limite_mensagem("Paciente incluído com sucesso!")
        except Exception as e:
            self.__limite_paciente.limite_mensagem(f"Ocorreu um erro ao tentar cadastrar o Paciente: {e}")
    
    def listar_pacientes(self):
        self.__limite_paciente.exibir_pacientes(self.__pacientes)

    def alterar_paciente(self):
        paciente = self.buscar_paciente(self.__limite_paciente.escolher_paciente())
        if paciente is None:
            self.__limite_paciente.limite_mensagem("Paciente não encontrado.")
            return
        dados = self.__limite_paciente.coletar_dados_paciente()
        if dados is None:
            return
        if dados["cpf"] != paciente.cpf and self.buscar_paciente(dados["cpf"]) is not None:
            self.__limite_paciente.limite_mensagem("Já existe um paciente com esse CPF.")
            return
        paciente.nome = dados["nome"]
        paciente.celular = dados["celular"]
        paciente.cpf = dados["cpf"]
        paciente.data_nasc = dados["data_nasc"]
        self.__limite_paciente.limite_mensagem("Paciente alterado com sucesso.")

    def excluir_paciente(self):
        paciente = self.buscar_paciente(self.__limite_paciente.escolher_paciente())
        if paciente is None:
            self.__limite_paciente.limite_mensagem("Paciente não encontrado.")
            return
        self.__pacientes.remove(paciente)
        self.__limite_paciente.limite_mensagem("Paciente excluído com sucesso.")
 
 
    def buscar_paciente(self, cpf: str) -> Paciente:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None

    def abre_menu(self):
        opcoes = {
            1: self.incluir_paciente,
            2: self.listar_pacientes,
            3: self.alterar_paciente,
            4: self.excluir_paciente,
        }

        while True:
            opcao = self.__limite_paciente.limite_opcoes()
            

            if opcao == 0:
                break
            funcao_escolhida = opcoes.get(opcao)
            
            if funcao_escolhida:
                funcao_escolhida()
    
            else:
                self.__limite_paciente.limite_mensagem("Opção inválida! Digite um número válido.")

    