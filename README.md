# Buscador de Cédulas - Leilões BR 💰

Este projeto consiste em um sistema de **web scraping** para buscar cédulas em leilões online, desenvolvido como requisito avaliativo para a disciplina de **Linguagem de Programação 2** da **Fatec Rio Claro**.

O objetivo principal é aplicar os conceitos de **Orientação a Objetos** e **raspagem de dados web** (web scraping) usando as bibliotecas `requests` e `BeautifulSoup`, além de praticar manipulação de arquivos e expressões regulares.

---

## 🛠️ Funcionalidades do Sistema

- **Busca por país:** O usuário digita o país da cédula que procura (ex: `argentina`, `brasil`, `uganda`).
- **Filtros combináveis:** É possível adicionar vários filtros ao mesmo tempo para refinar a busca:
  - **Ano** da cédula (ex: `1960`, `1990`)
  - **Pick** (código internacional de catálogo, ex: `216`)
  - **Estado de conservação** (FE, SOB, MBC, BC, etc.)
  - **Leiloeiro** (nome do vendedor, ex: `ana aquino`)
  - **Data limite** de encerramento do leilão (ex: `30/9/2026`)
- **Paginação automática:** O programa percorre todas as páginas de resultados do site automaticamente (21 itens por página).
- **Ordenação por data:** Os resultados são exibidos em ordem crescente de encerramento (os mais próximos primeiro).
- **Exibição paginada no terminal:** Os lotes são mostrados de 8 em 8, com opção de avançar, mostrar todos ou parar.
- **Salvamento em TXT:** Os resultados podem ser salvos em arquivo de texto com cabeçalho formatado e todos os dados dos lotes.
- **Aceita vários formatos de data:** O filtro de data limite aceita `30/9/2026`, `30/09/2026`, `30/09/26`, `2026-09-30`, etc.

---

## 🧠 Diferenciais Técnicos e Usabilidade

- **Arquitetura Orientada a Objetos:** O projeto usa duas classes principais (`Lote` e `Busca`), cada uma com atributos e métodos bem definidos, aplicando os pilares de **abstração** e **encapsulamento**.
- **Separação de responsabilidades (SoC):** Cada arquivo tem uma função clara:
  - `lote.py` → representa um lote individual (dados + extração)
  - `busca.py` → encapsula toda a lógica de raspagem e filtragem
  - `scraper.py` → menus, prompts e exibição de resultados
- **Filtro com expressão regular:** O filtro de estado de conservação usa regex com `\b` (borda de palavra) para evitar falsos positivos como "fe" em "diferentes".
- **Busca case-insensitive:** O usuário pode digitar `ARGENTINA`, `Argentina` ou `argentina` que o sistema reconhece.
- **Robustez:** Tratamento de exceções com `try/except` para erros de rede, timeout e datas inválidas.
- **Cabeçalho User-Agent:** O programa simula um navegador real para evitar bloqueios do site.

---

## 🏗️ Estrutura Orientada a Objetos

O projeto foi construído com duas classes principais:

1. **Classe `Lote`** (`lote.py`): Representa um lote individual de cédula, com os atributos:
   - `titulo` — título completo do lote
   - `preco` — preço atual
   - `data` — data de encerramento (objeto `datetime`)
   - `leiloeiro` — nome do leiloeiro
   - `link` — URL completa para o lote

2. **Classe `Busca`** (`busca.py`): Representa uma busca completa, com os atributos:
   - `pais` — país pesquisado
   - `termo` — termo formatado para o site
   - `filtros` — dicionário com os filtros ativos
   - `lotes` — lista de objetos `Lote` encontrados

   Métodos principais: `executar()`, `adicionar_filtro()`, `limpar_filtros()`, `salvar_txt()`.

---

## 📁 Estrutura do Projeto

```text
mini_projeto_01/
├── lote.py             # Classe Lote (representa um lote individual)
├── busca.py            # Classe Busca (encapsula raspagem e filtragem)
├── scraper.py          # Programa principal (menus e exibição)
├── requirements.txt    # Dependências do projeto
├── README.md           # Esta documentação
├── INSTALACAO.md       # Como instalar e executar
├── COMO_USAR.md        # Roteiro de teste passo a passo
└── .gitignore          # Arquivos ignorados pelo Git
```

---

## 🚀 Como Executar o Projeto

Para instruções detalhadas de **instalação passo a passo** (clone, ambiente virtual, dependências e execução), consulte o arquivo [**INSTALACAO.md**](INSTALACAO.md).

### Resumo rápido

```bash
git clone https://github.com/elieltonestudo-maker/mini_projeto_01.git
cd mini_projeto_01
python -m venv venv
venv\Scripts\Activate.ps1     # Windows PowerShell
# ou: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python scraper.py
```

---

## 📖 Documentação adicional

- [**INSTALACAO.md**](INSTALACAO.md) — Como clonar, instalar e rodar o projeto na sua máquina
- [**COMO_USAR.md**](COMO_USAR.md) — Roteiro de teste e funcionalidades do sistema

---

## 🧑‍💻 Desenvolvedor

- **Nome:** Elielton Barbosa
- **Instituição:** Fatec Rio Claro
- **Disciplina:** Linguagem de Programação 2
- **Professor:** Orlando Saraiva Júnior
- **Semestre:** 2º semestre de 2026

---

## 📚 Bibliotecas Utilizadas

- **requests** — para baixar as páginas HTML do site
- **beautifulsoup4** — para analisar e extrair informações do HTML
- **re** (nativa) — para expressões regulares (filtro de estado)
- **datetime** (nativa) — para manipulação de datas

---

## ⚠️ Observações

- O site **Leilões BR** é atualizado com frequência. Se a estrutura HTML mudar, o código pode precisar de ajustes.
- Alguns títulos aparecem com **reticências (...)** porque foram cadastrados assim pelo próprio vendedor, não por limitação do scraper.
- A busca por **ano** depende do vendedor ter colocado o ano no título do lote. Nem todos os lotes têm essa informação explícita.
- O programa respeita boas práticas de web scraping: define um User-Agent, faz requisições paginadas e tem timeout configurado.