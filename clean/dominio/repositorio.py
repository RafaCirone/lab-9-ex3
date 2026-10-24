"""Abstração (DIP): o núcleo define o contrato; a infraestrutura o implementa."""
from abc import ABC, abstractmethod
from typing import Optional

from dominio.entidades import Conta


class IContaRepository(ABC):
    """Interface de persistência de contas. O domínio e os casos de uso
    dependem apenas dela, nunca de um arquivo, banco SQL etc."""

    @abstractmethod
    def salvar(self, conta: Conta) -> None:
        """Insere ou atualiza a conta."""

    @abstractmethod
    def buscar(self, numero: int) -> Optional[Conta]:
        """Busca a conta pelo número. Devolve None se não existir."""

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[Conta]:
        """Busca a conta pelo CPF do titular. Devolve None se não existir."""

    @abstractmethod
    def proximo_numero(self) -> int:
        """Devolve um número livre para uma nova conta."""
