"""Domínio: entidades do banco. Não conhece arquivo, tela nem framework."""
from datetime import datetime


class DominioError(Exception):
    """Erro lançado quando uma regra do banco é violada."""


class Cliente:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"


class Transacao:
    """Registro imutável de uma operação feita na conta."""

    DEPOSITO = "Depósito"
    SAQUE = "Saque"
    ABERTURA = "Abertura"

    def __init__(self, tipo: str, valor: float, saldo_apos: float, data: datetime = None):
        self._tipo = tipo
        self._valor = valor
        self._saldo_apos = saldo_apos
        self._data = data or datetime.now()

    @property
    def tipo(self):
        return self._tipo

    @property
    def valor(self):
        return self._valor

    @property
    def saldo_apos(self):
        return self._saldo_apos

    @property
    def data(self):
        return self._data


class Conta:
    """Entidade central. Ela mesma protege suas regras (valor > 0, sem saldo negativo)."""

    def __init__(self, numero: int, cliente: Cliente, saldo_inicial: float = 0.0,
                 historico=None):
        if saldo_inicial < 0:
            raise DominioError("O saldo inicial não pode ser negativo.")
        self.numero = numero
        self.cliente = cliente
        self._saldo = saldo_inicial
        # historico é passado ao recarregar uma conta já existente
        self._historico = list(historico) if historico else [
            Transacao(Transacao.ABERTURA, saldo_inicial, saldo_inicial)
        ]

    @property
    def saldo(self) -> float:
        """Somente leitura: o saldo só muda por depositar/sacar."""
        return self._saldo

    @property
    def historico(self):
        """Somente leitura: devolve uma cópia da lista de transações."""
        return list(self._historico)

    def depositar(self, valor: float):
        if valor <= 0:
            raise DominioError("O valor do depósito deve ser maior que zero.")
        self._saldo += valor
        self._historico.append(Transacao(Transacao.DEPOSITO, valor, self._saldo))

    def sacar(self, valor: float):
        if valor <= 0:
            raise DominioError("O valor do saque deve ser maior que zero.")
        if valor > self._saldo:
            raise DominioError("Saldo insuficiente para realizar o saque.")
        self._saldo -= valor
        self._historico.append(Transacao(Transacao.SAQUE, valor, self._saldo))

    def __str__(self):
        return f"Conta {self.numero} - {self.cliente.nome}"
