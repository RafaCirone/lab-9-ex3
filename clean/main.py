"""Composição: único lugar que conhece as implementações concretas."""
import os
import tkinter as tk

from infraestrutura.arquivo_conta_repository import ArquivoContaRepository
from aplicacao.casos_de_uso import (
    BuscarContaUseCase, ConsultarHistoricoUseCase, CriarContaUseCase,
    DepositarUseCase, RealizarSaqueUseCase,
)
from apresentacao.controller import BancoController
from apresentacao.view import BancoView

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contas.txt")


def main():
    # Trocar ArquivoContaRepository por outra implementação de
    # IContaRepository (SQL, memória...) não muda nada no domínio.
    repositorio = ArquivoContaRepository(ARQUIVO_DADOS)

    root = tk.Tk()
    view = BancoView(root)
    BancoController(
        view,
        criar_conta=CriarContaUseCase(repositorio),
        buscar_conta=BuscarContaUseCase(repositorio),
        depositar=DepositarUseCase(repositorio),
        sacar=RealizarSaqueUseCase(repositorio),
        historico=ConsultarHistoricoUseCase(repositorio),
    )
    root.mainloop()


if __name__ == "__main__":
    main()
