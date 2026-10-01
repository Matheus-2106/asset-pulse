# AssetPulse - Monitor de Investimentos Inteligente

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pydantic](https://img.shields.io/badge/Pydantic-v2.6-red?style=for-the-badge)
![Pytest](https://img.shields.io/badge/Pytest-Passing-brightgreen?style=for-the-badge&logo=pytest)
![License](https://img.shields.io/badge/License-GPL--3.0-blue?style=for-the-badge)

**AssetPulse** é uma aplicação em Python desenvolvida para monitorar cotações, calcular métricas financeiras em tempo real (Ações B3, Fundos Imobiliários e Criptomoedas) e apresentar dados estruturados diretamente no terminal.

O projeto foi construído seguindo princípios de **Clean Architecture**, **imutabilidade com Pydantic**, **resiliência a falhas de rede** e **cobertura de testes unitários**.

---

## Funcionalidades Principais

- **Cotações em Tempo Real:** Consulta automatizada a APIs públicas financeiras (Yahoo Finance).
- **Suporte Multiativo:** Cobertura de Ações da B3 (PETR4, VALE3), Ações Internacionais (AAPL, TSLA), FIIs (HGLG11, MXRF11) e Criptomoedas (BTC-USD, ETH-USD).
- **Interface de Terminal Interativa (CLI):** Renderização de tabelas e cores condicionais (alta/baixa) utilizando a biblioteca `Rich`.
- **Modo de Linha de Comando (Fast Query):** Execução direta via argumentos de terminal sem navegar pelos menus.
- **Tipagem e Validação:** Data Transfer Objects (DTOs) estritamente validados com `Pydantic`.
- **Testes Automatizados:** Suíte de testes unitários cobrindo regras de negócio e chamadas HTTP mockadas.

---

## Arquitetura do Sistema

```text
[Usuário / CLI] -->|Argumentos / Menu| [app/cli.py]
  -->|Solicita Cotação| [Services: FinanceAPIService]
  -->|Requisição HTTP Resiliente| [API Pública / Yahoo Finance]
  -->|Payload JSON| [Services: FinanceAPIService]
  -->|Mapeia & Valida| [Models: AssetQuote DTO]
  -->|Métricas & Propriedades| [app/cli.py]
  -->|Formatação & Cores| [Utils: Formatters]
  -->|Renderiza Tabela| [Terminal / Console Rich]
```

---

## Estrutura do Projeto

```text
asset-pulse/
├── app/
│   ├── __init__.py
│   ├── cli.py            # Ponto de entrada e interface do usuário (CLI)
│   ├── config.py         # Variáveis de ambiente e configurações globais
│   ├── models.py         # Modelos de dados e validações (Pydantic DTOs)
│   ├── services/
│   │   ├── __init__.py
│   │   └── finance_api.py # Cliente HTTP para consumo de APIs financeiras
│   └── utils/
│       ├── __init__.py
│       └── formatters.py # Utilitários de formatação monetária e estilo
├── tests/
│   ├── __init__.py
│   ├── test_finance_api.py # Testes do cliente HTTP com Mocks
│   ├── test_formatters.py  # Testes dos formatadores de texto
│   └── test_models.py      # Testes de integridade dos modelos Pydantic
├── .gitignore            # Regras de exclusão do Git
├── LICENSE               # Licença GNU GPL v3.0
├── README.md             # Documentação do projeto
└── requirements          # Dependências da aplicação
```

---

## Como Executar

### 1. Clonar o Repositório
```bash
git clone git@github.com:matheus-2106/asset-pulse.git
cd asset-pulse
```

### 2. Configurar o Ambiente Virtual

```bash
# Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux
# ou .venv\Scripts\activate # Windows

# Instalar dependências
pip install -r requirements
```

> **Nota para uso em IDEs (PyCharm / VS Code):**
> No PyCharm, abra o terminal integrado da IDE. Ele ativará o ambiente `.venv` automaticamente.

### 3. Executando a Aplicação

**Modo Interativo:**
```bash
python -m app.cli
```

**Modo Direto via Argumentos:**
```bash
# Consultar Ação Brasileira
python -m app.cli -t PETR4

# Consultar Criptomoeda
python -m app.cli -t BTC-USD --asset-type crypto
```

---

## Executando os Testes Automatizados

Para rodar a suíte completa de testes unitários:

```bash
pytest
```

Para visualizar o relatório detalhado de execução:
```bash
pytest -v
```

---

## Licença

Este projeto está sob a licença **GNU General Public License v3.0** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.