# Mini Projeto 01 - Buscador de Cédulas

Projeto de web scraping que busca cédulas no site Leilões BR.

## Requisitos

- Python 3.8 ou superior instalado
- Conexão com a internet

## Como instalar

### 1. Clonar o repositório (primeira vez)

Abra o **CMD** ou o **VS Code** na pasta onde quer salvar o projeto e rode:

```
git clone https://github.com/elieltonestudo-maker/mini_projeto_01.git
cd mini_projeto_01
```

### 2. Instalar as bibliotecas necessárias

Ainda no terminal, rode:

```
pip install -r requirements.txt
```

Se o `pip` não for reconhecido, tente:

```
python -m pip install -r requirements.txt
```

No Linux/Mac, use `pip3` no lugar de `pip`.

## Como executar

### Opção A - Pelo CMD (Windows)

1. Abra o CMD na pasta do projeto (Shift + clique direito → "Abrir janela do PowerShell aqui")
2. Rode:
   ```
   python scraper.py
   ```
3. Siga as instruções do menu que aparecer na tela.

### Opção B - Pelo VS Code

1. Abra o VS Code
2. Menu **File** → **Open Folder** → selecione a pasta `mini_projeto_01`
3. Abra o terminal integrado com **Ctrl + `** (crase)
4. Rode:
   ```
   python scraper.py
   ```
5. Siga as instruções do menu que aparecer na tela.

## Como usar o programa

Ao executar, o programa vai pedir:

1. **País da cédula** — digite o nome do país (ex: `argentina`, `brasil`)
2. **Tipo de refinamento** — escolha uma das opções:
   - `1` — Buscar por ano
   - `2` — Buscar por Pick (código internacional)
   - `3` — Buscar por estado de conservação
   - `4` — Buscar só pelo país
   - `0` — Sair
3. Dependendo da escolha, o programa vai pedir mais um dado (o ano, o número do Pick, ou o estado).

Ao final, o programa mostra os lotes encontrados com **título, preço, leiloeiro e link**.

## Bibliotecas usadas

- **requests** — para baixar as páginas da web
- **beautifulsoup4** — para ler e extrair informações do HTML

## Estrutura do projeto

```
mini_projeto_01/
├── scraper.py          # código principal
├── requirements.txt    # bibliotecas necessárias
├── README.md           # este arquivo
└── .gitignore          # arquivos ignorados pelo git
```

## Observações

- O site Leilões BR é atualizado com frequência; se o HTML mudar, o código pode precisar de ajustes.
- A busca por ano depende do vendedor ter colocado o ano no título do lote.