# Explicação do Código 📖

Este documento explica **o que cada arquivo, classe, método e função faz** no projeto. É um guia de leitura do código, útil pra quem está aprendendo ou quer entender a arquitetura.

---

## 🗂️ Arquivos do projeto

| Arquivo | Responsabilidade |
|---------|------------------|
| `lote.py` | Representa **um lote individual** de cédula |
| `busca.py` | Encapsula **toda** a lógica de raspagem, filtragem e salvamento |
| `scraper.py` | Menus, prompts e exibição (interface com o usuário) |

**Fluxo de dependência:**
```
scraper.py  →  importa  →  busca.py  →  importa  →  lote.py
```

- `scraper.py` **pede dados** e **mostra resultados**
- `busca.py` **faz o trabalho pesado** (baixar, filtrar, ordenar)
- `lote.py` **representa** cada item individual

---

## 📄 1. `lote.py` — Classe `Lote`

**Responsabilidade:** representar um lote individual de cédula. Pega a tag HTML que o BeautifulSoup devolve e extrai os dados.

### `class Lote:`

Define a classe. Tudo dentro dela é sobre **um** lote.

### `def __init__(self, tag_html):`

**Construtor.** Roda automaticamente quando você faz `Lote(tag_html)`. Chama os 5 métodos privados e guarda os dados como **atributos** (`self.titulo`, `self.preco`, etc.).

### `def _pegar_titulo(self, tag_html):`

Extrai o **título completo** do lote. Pega o atributo `data-bs-original-title` (que tem o título sem truncar) e, se não existir, usa o texto do `<h3>`.

### `def _pegar_preco(self, tag_html):`

Extrai o **preço**. Procura a `<div class="venda-price">` e pega o texto (ex: `R$ 12,00`).

### `def _pegar_data(self, tag_html):`

Extrai a **data de encerramento**. Pega o texto `28/9/2026 - 20h - RS`, corta antes do primeiro `-`, e converte para `datetime`. Se der erro, retorna `None`.

### `def _pegar_leiloeiro(self, tag_html):`

Extrai o **nome do leiloeiro**. Pega todas as `<div class="mostbidded__info">`, usa a **última** (que é o leiloeiro), e pega o texto do `<a>` dentro dela.

### `def _pegar_link(self, tag_html):`

Extrai o **link completo**. Pega o `href` do `<a class="stretched-link">`. Se for relativo, concatena com `https://leiloesbr.com.br/`.

### `def data_formatada(self):`

**Método público.** Devolve a data como string `DD/MM/AAAA` ou `"(sem data)"`. Usado na hora de exibir e salvar.

### `def preco_numerico(self):`

**Método público.** Converte o preço (`"R$ 12,00"`) em número (`12.0`). Usado pelo filtro de faixa de preço. Trata:
- Remove `R$` e espaços
- Remove o ponto de milhar
- Troca a vírgula por ponto decimal
- Retorna `None` se não conseguir converter

---

## 📄 2. `busca.py` — Classe `Busca`

**Responsabilidade:** encapsular **toda** a lógica de buscar, filtrar, ordenar e salvar.

### Constantes no topo do arquivo

| Constante | O que é |
|-----------|---------|
| `ENDERECO_BUSCA` | URL base do site |
| `CABECALHO` | User-Agent pra simular navegador |
| `PADROES_ESTADO` | Dicionário com regex de cada estado (FE, SOB, MBC, BC, regular) |

### `class Busca:`

Define a classe. Tudo dentro dela é sobre **uma busca completa**.

### `def __init__(self, pais):`

**Construtor.** Inicializa:
- `self.pais` — país digitado
- `self.termo` — `"argentina cedula"` (termo formatado pro site)
- `self.filtros` — dicionário com todos os filtros começando como `None`
- `self.lotes` — lista vazia (será preenchida depois)

### `def adicionar_filtro(self, nome, valor):`

Guarda o valor de um filtro específico. Ex: `busca.adicionar_filtro("estado", "fe")`.

### `def limpar_filtros(self):`

Reseta todos os filtros para `None`.

### `def tem_filtro_ativo(self):`

Devolve `True` se **pelo menos um** filtro está ativo. Usado pra decidir se vale a pena filtrar.

### `def executar(self):`

**Método principal.** Chama em sequência:
1. `_baixar_todas_paginas()` — baixa tudo
2. `_filtrar_cedulas()` — remove não-cédulas
3. `_aplicar_filtros()` — aplica os filtros escolhidos
4. `.sort()` — ordena por data crescente
5. Imprime contagens e retorna a lista

### `def _baixar_pagina(self, pagina=1):`

Faz o `requests.get()` de **uma** página. Passa `op=2`, `pesquisa`, `v=21`, `pag=N`. Trata erro com `try/except`.

### `def _baixar_todas_paginas(self):`

Loop que baixa páginas 1, 2, 3... até uma vir vazia. Cria um `Lote(tag)` pra cada tag HTML. Limite de segurança: para depois de 20 páginas.

### `def _filtrar_cedulas(self):`

Remove lotes que **não** têm "cédula" (com/sem acento, singular/plural) no título. Evita pegar moedas, selos, etc.

### `def _aplicar_filtros(self):`

Para cada lote, verifica se passa em **todos** os filtros ativos:
- **ano** — busca substring no título
- **pick** — busca `216` ou `p-216` no título
- **estado** — usa regex (ex: `\bfe\b|\bflor de estampa\b`)
- **leiloeiro** — busca substring no nome do leiloeiro
- **data_limite** — compara `lote.data` com a data convertida
- **palavra_chave** — busca substring no título
- **preco_min / preco_max** — usa `lote.preco_numerico()` para comparar

### `def salvar_txt(self, nome_arquivo):`

Escreve um `.txt` com:
- **Cabeçalho** — país, filtros aplicados, total, data da busca
- **Cada lote** — título, preço, data formatada, leiloeiro, link

---

## 📄 3. `scraper.py` — Programa principal

**Responsabilidade:** menus, prompts e exibição. Chama a classe `Busca`.

### Imports

- `datetime` — pra converter data no `converter_data`
- `from busca import Busca` — a classe principal

### `def mostrar_menu_principal():`

Imprime o menu inicial (1 - Buscar / 0 - Sair) e devolve a opção.

### `def pedir_pais():`

Pede o país e devolve em minúsculas (`strip().lower()`).

### `def pedir_ano()` / `pedir_pick()` / `pedir_leiloeiro()` / `pedir_data_limite()`

Cada uma pede um valor específico do usuário e devolve a string.

### `def pedir_palavra_chave()`

Pede um termo livre para o usuário (ex: `polimero`, `maria eva`). Devolve em minúsculas.

### `def pedir_faixa_preco()`

Pede o preço mínimo e máximo. **Tem um loop `while True` que repete até a faixa ser válida.** Valida:
- Valores numéricos (usa `converter_preco`)
- Mínimo não pode ser maior que o máximo
- Aceita Enter nos dois para cancelar (retorna `(None, None)`)

### `def converter_preco(texto)`

Converte texto (`"10"`, `"10,50"`, `"R$ 10,00"`) em `float`. Retorna `None` se não conseguir.

### `def mostrar_menu_estado():`

Imprime o submenu de estados (FE, SOB, MBC, BC, outro) e devolve a opção.

### `def escolher_estado():`

Traduz a opção numérica do menu pra **sigla** (`1 → "fe"`, `2 → "sob"`, etc.). Se escolher "5", pede digitação.

### `def converter_data(texto):`

Tenta converter o texto em `datetime` testando **6 formatos** (`30/9/2026`, `30/09/26`, `2026-09-30`, etc.). Se nenhum funcionar, retorna `None`.

### `def mostrar_resumo_filtros(pais, filtros):`

Mostra o **estado atual** dos filtros (quais estão ativos) e o menu de opções (1-9 + 0).

### `def escolher_filtros(pais):`

**Loop principal de filtros.** Deixa o usuário adicionar/limpar filtros até escolher "8 - Buscar agora". Devolve o dicionário de filtros ou `None` (cancelou).

### `def mostrar_resultados(lotes, busca):`

**Exibe os lotes de 8 em 8.** A cada bloco, pergunta `[Enter] Próximos / [t] Todos / [s] Salvar / [q] Parar`. Se `s`, chama `busca.salvar_txt()`. No final, pergunta se quer salvar.

### `def buscar_cedulas():`

**Fluxo principal:**
1. Pede o país
2. Abre o menu de filtros (`escolher_filtros`)
3. Cria `Busca(pais)` e passa os filtros escolhidos
4. Chama `busca.executar()`
5. Chama `mostrar_resultados(lotes, busca)`

### `def main():`

**Loop principal.** Roda o menu até o usuário digitar `0`. Chama `buscar_cedulas()` se for `1`.

### `if __name__ == "__main__": main()`

Garante que `main()` só roda se o arquivo for executado direto (não se for importado).

---

## 🔗 Como os arquivos se conectam

```
scraper.py  (interface)
     ↓ importa
busca.py    (lógica)
     ↓ importa
lote.py     (dados)
```

Cada um tem uma responsabilidade clara — isso se chama **Separação de Responsabilidades (SoC)**, um princípio importante de POO.

---

## 🎯 Conceitos de POO aplicados

| Conceito | Onde aparece |
|----------|--------------|
| **Abstração** | `Lote` e `Busca` representam conceitos reais do domínio |
| **Encapsulamento** | Atributos (`self.pais`, `self.lotes`) e métodos privados (`_pegar_titulo`) |
| **Métodos** | `executar()`, `salvar_txt()`, `adicionar_filtro()` |
| **Atributos** | `self.titulo`, `self.preco`, `self.data`, `self.filtros` |
| **Construtor** | `__init__(self, pais)` e `__init__(self, tag_html)` |

---

## 📚 Bibliotecas usadas

| Biblioteca | Uso no projeto |
|-----------|----------------|
| `requests` | Baixar as páginas HTML do site |
| `beautifulsoup4` | Analisar e extrair dados do HTML |
| `re` (nativa) | Expressões regulares (filtro de estado) |
| `datetime` (nativa) | Manipulação de datas |