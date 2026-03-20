# finance-flow

## Sistema de Gerenciamento de Gastos

Este projeto é um sistema simples e eficiente para controle financeiro pessoal, desenvolvido em Python, utilizando SQLite, Pandas e Streamlit

O objetivo do sistema é permitir o acompanhamento de despesas de forma prática, oferecendo organização, análise financeira.

---

## Tecnologias Utilizadas

* Python — linguagem principal do projeto
* SQLite — banco de dados leve e local
* Pandas — manipulação e análise de dados
* Streamlit — interface web interativa

---

## Funcionalidades

### Cadastro de Dados

O sistema permite o cadastro de informações essenciais para organização financeira:

* Categorias (ex: Alimentação, Transporte, Lazer)
* Formas de pagamento (ex: Dinheiro, Cartão, PIX)
* Movimentações financeiras

---

### Gerenciamento de Movimentações

* Listagem completa das movimentações linha a linha
* Edição direta dos dados na mesma linha, facilitando ajustes rápidos
* Organização dos registros por período

---

### Análise de Dados

O sistema gera visualizações para facilitar o entendimento dos gastos:

* Gráfico de gastos por categoria
* Gráfico de gastos por forma de pagamento

Esses gráficos ajudam a identificar padrões e tomar decisões mais conscientes

Com base no período selecionado, o sistema apresenta:

* Valor total movimentado
* Quantidade de movimentações realizadas

---

## Estrutura do Sistema

O sistema é organizado em:

* Banco de dados SQLite para armazenamento
* Manipulação de dados com Pandas
* Interface interativa com Streamlit

---

## Como Executar o Projeto

1. Baixe ou clone o repositório
2. instale as dependências
3. utilize -> run.bat

```bash
pip install -r requirements.txt
```

---

## Possíveis Melhorias Futuras

* Exportação para excel
* Autenticação
* Filtro de pesquisa
* Controle de metas e orçamento
