"""Casos de uso: orquestram o domínio. Dependem só de IContaRepository."""
from dominio.entidades import Cliente, Conta, DominioError
from dominio.repositorio import IContaRepository


def _normalizar_cpf(cpf: str) -> str:
    return (cpf or "").replace(".", "").replace("-", "").strip()


class BuscarContaUseCase:
    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, termo: str) -> Conta:
        termo = _normalizar_cpf(termo)
        if not termo:
            raise DominioError("Informe o número da conta ou o CPF.")

        conta = None
        if termo.isdigit() and len(termo) == 11:
            conta = self.repositorio.buscar_por_cpf(termo)
        elif termo.isdigit():
            conta = self.repositorio.buscar(int(termo))

        if conta is None:
            raise DominioError("Conta não encontrada.")
        return conta


class CriarContaUseCase:
    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio

    def executar(self, nome: str, cpf: str, saldo_inicial: float) -> Conta:
        nome = (nome or "").strip()
        if not nome:
            raise DominioError("Informe o nome do titular.")

        cpf = _normalizar_cpf(cpf)
        if not cpf.isdigit() or len(cpf) != 11:
            raise DominioError("CPF inválido. Informe 11 dígitos.")

        if self.repositorio.buscar_por_cpf(cpf):
            raise DominioError("Já existe uma conta cadastrada para este CPF.")

        conta = Conta(self.repositorio.proximo_numero(), Cliente(nome, cpf), saldo_inicial)
        self.repositorio.salvar(conta)
        return conta


class DepositarUseCase:
    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio
        self._buscar = BuscarContaUseCase(repositorio)

    def executar(self, termo: str, valor: float) -> Conta:
        conta = self._buscar.executar(termo)
        conta.depositar(valor)
        self.repositorio.salvar(conta)
        return conta


class RealizarSaqueUseCase:
    """Depende apenas da interface IContaRepository (DIP)."""

    def __init__(self, repositorio: IContaRepository):
        self.repositorio = repositorio
        self._buscar = BuscarContaUseCase(repositorio)

    def executar(self, termo: str, valor: float) -> Conta:
        conta = self._buscar.executar(termo)
        conta.sacar(valor)              # a regra de saldo fica na entidade
        self.repositorio.salvar(conta)
        return conta


class ConsultarHistoricoUseCase:
    def __init__(self, repositorio: IContaRepository):
        self._buscar = BuscarContaUseCase(repositorio)

    def executar(self, termo: str):
        conta = self._buscar.executar(termo)
        return conta, conta.historico
