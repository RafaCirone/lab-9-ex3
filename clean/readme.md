# Sistema Bancário - Clean Architecture (Python)

Exercício 3: refatoração do sistema bancário para **Clean Architecture**, aplicando o
**Princípio da Inversão de Dependência (DIP)**. Os dados agora são salvos no arquivo
`contas.txt`, então as contas continuam existindo depois de fechar o programa.

## Estrutura

```
clean/
├── dominio/                          # NÚCLEO (não depende de nada externo)
│   ├── entidades.py                  # Cliente, Conta, Transacao, DominioError
│   └── repositorio.py                # IContaRepository (interface / abstração)
├── aplicacao/
│   └── casos_de_uso.py               # RealizarSaqueUseCase, DepositarUseCase, CriarContaUseCase...
├── infraestrutura/
│   └── arquivo_conta_repository.py   # ArquivoContaRepository: implementa a interface com TXT
├── apresentacao/
│   ├── controller.py                 # Converte o texto da tela e chama os casos de uso
│   └── view.py                       # Interface Tkinter
├── main.py                           # Composição: liga as implementações concretas
└── contas.txt                        # Criado automaticamente na primeira gravação
```

## Como o DIP foi aplicado

- **Abstração:** `IContaRepository` (classe abstrata com `salvar`, `buscar`,
  `buscar_por_cpf` e `proximo_numero`) fica no domínio.
- **Domínio:** `Conta` e `Cliente` ficam no centro. A própria `Conta` protege suas regras
  (valor maior que zero, sem saque acima do saldo).
- **Caso de uso:** `RealizarSaqueUseCase` recebe um `IContaRepository` no construtor e não
  importa nada de arquivo, Tkinter ou infraestrutura.
- **Infraestrutura:** `ArquivoContaRepository` implementa a interface gravando em TXT.

As dependências apontam para dentro:
`apresentacao -> aplicacao -> dominio <- infraestrutura`.
Só o `main.py` conhece a classe concreta; trocar o TXT por um banco SQL seria criar outra
classe que implementa `IContaRepository` e mudar uma linha no `main.py`.

## Formato do contas.txt

```
CONTA;1001;Maria Silva;12345678901;150.0
TRANSACAO;1001;Abertura;100.0;100.0;2026-10-24T19:30:00
TRANSACAO;1001;Depósito;50.0;150.0;2026-10-24T19:31:10
```

## Como executar

Requer Python 3.8+ (Tkinter já vem com o Python). De dentro da pasta `clean`:

```bash
python main.py
```

Para recomeçar do zero, apague o arquivo `contas.txt`.
