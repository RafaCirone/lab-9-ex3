"""Infraestrutura: implementação real de IContaRepository usando um arquivo TXT.

Formato do arquivo (um registro por linha, campos separados por ';'):
    CONTA;numero;nome;cpf;saldo
    TRANSACAO;numero;tipo;valor;saldo_apos;data_iso
"""
import os
from datetime import datetime
from typing import Dict, Optional

from dominio.entidades import Cliente, Conta, Transacao
from dominio.repositorio import IContaRepository

SEP = ";"


class ArquivoContaRepository(IContaRepository):
    def __init__(self, caminho: str):
        self.caminho = caminho
        self._contas: Dict[int, Conta] = {}
        self._carregar()

    # ---------------- interface ----------------
    def salvar(self, conta: Conta) -> None:
        self._contas[conta.numero] = conta
        self._gravar()

    def buscar(self, numero: int) -> Optional[Conta]:
        return self._contas.get(numero)

    def buscar_por_cpf(self, cpf: str) -> Optional[Conta]:
        for conta in self._contas.values():
            if conta.cliente.cpf == cpf:
                return conta
        return None

    def proximo_numero(self) -> int:
        return max(self._contas, default=1000) + 1

    # ---------------- leitura / escrita do TXT ----------------
    def _carregar(self):
        if not os.path.exists(self.caminho):
            return
        dados = {}  # numero -> (cliente, saldo, [transacoes])
        with open(self.caminho, encoding="utf-8") as arq:
            for linha in arq:
                campos = linha.rstrip("\n").split(SEP)
                if campos[0] == "CONTA":
                    _, numero, nome, cpf, saldo = campos
                    dados[int(numero)] = (Cliente(nome, cpf), float(saldo), [])
                elif campos[0] == "TRANSACAO":
                    _, numero, tipo, valor, saldo_apos, data = campos
                    dados[int(numero)][2].append(Transacao(
                        tipo, float(valor), float(saldo_apos), datetime.fromisoformat(data)))
        for numero, (cliente, saldo, transacoes) in dados.items():
            conta = Conta(numero, cliente, saldo, historico=transacoes)
            self._contas[numero] = conta

    def _gravar(self):
        pasta = os.path.dirname(self.caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        temporario = self.caminho + ".tmp"
        with open(temporario, "w", encoding="utf-8") as arq:
            for conta in self._contas.values():
                nome = conta.cliente.nome.replace(SEP, ",")
                arq.write(SEP.join(["CONTA", str(conta.numero), nome,
                                    conta.cliente.cpf, repr(conta.saldo)]) + "\n")
                for t in conta.historico:
                    arq.write(SEP.join(["TRANSACAO", str(conta.numero), t.tipo,
                                        repr(t.valor), repr(t.saldo_apos),
                                        t.data.isoformat()]) + "\n")
        os.replace(temporario, self.caminho)  # troca atômica: não corrompe o arquivo
