"""Adaptador de interface: converte o texto da tela em valores e chama os casos de uso."""
from dominio.entidades import DominioError


def _converter_valor(texto: str, campo: str) -> float:
    if not texto:
        raise DominioError(f"Informe o {campo.lower()}.")
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        raise DominioError(f"{campo} deve ser um número.")


class BancoController:
    def __init__(self, view, criar_conta, buscar_conta, depositar, sacar, historico):
        self.view = view
        self.criar_conta_uc = criar_conta
        self.buscar_conta_uc = buscar_conta
        self.depositar_uc = depositar
        self.sacar_uc = sacar
        self.historico_uc = historico
        self.view.set_controller(self)

    def _executar(self, acao):
        try:
            return acao()
        except DominioError as erro:
            self.view.exibir_erro(str(erro))
            return None

    def criar_conta(self):
        conta = self._executar(lambda: self.criar_conta_uc.executar(
            self.view.ler_nome(), self.view.ler_cpf(),
            _converter_valor(self.view.ler_saldo(), "Saldo inicial")))
        if conta:
            self.view.exibir_conta(conta)
            self.view.limpar_campos()
            self.view.exibir_mensagem(f"Conta {conta.numero} criada com sucesso!")

    def consultar_conta(self):
        conta = self._executar(lambda: self.buscar_conta_uc.executar(self.view.ler_busca()))
        if conta:
            self.view.exibir_conta(conta)

    def depositar(self):
        conta = self._executar(lambda: self.depositar_uc.executar(
            self.view.ler_busca(), _converter_valor(self.view.ler_valor(), "Valor")))
        if conta:
            self.view.limpar_valor()
            self.view.exibir_conta(conta)
            self.view.exibir_mensagem("Depósito realizado com sucesso!")

    def sacar(self):
        conta = self._executar(lambda: self.sacar_uc.executar(
            self.view.ler_busca(), _converter_valor(self.view.ler_valor(), "Valor")))
        if conta:
            self.view.limpar_valor()
            self.view.exibir_conta(conta)
            self.view.exibir_mensagem("Saque realizado com sucesso!")

    def ver_historico(self):
        resultado = self._executar(lambda: self.historico_uc.executar(self.view.ler_busca()))
        if resultado:
            self.view.exibir_historico(*resultado)
