# Como Rodar o Projeto na Sua Máquina 🚀

Este guia mostra **passo a passo** como clonar o repositório, instalar as dependências e executar o projeto na sua máquina.

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- [**Python 3.8 ou superior**](https://www.python.org/downloads/)
  - ⚠️ **Importante:** ao instalar o Python no Windows, marque a opção **"Add Python to PATH"** durante a instalação
- [**Git**](https://git-scm.com/downloads)

### Como verificar se já tem instalado

Abra o **CMD** (Windows) ou o **terminal** (Linux/Mac) e digite:

```bash
python --version
git --version
```

**Esperado:**
- `Python 3.x.x` (alguma versão 3.8 ou superior)
- `git version 2.x.x`

Se aparecer **"comando não encontrado"** ou **"não é reconhecido"**, instale pela página oficial.

---

## 📥 Passo 1 — Clonar o repositório

Abra o **CMD** (ou terminal) na pasta onde quer salvar o projeto (ex: `Documentos`):

```bash
git clone https://github.com/elieltonestudo-maker/mini_projeto_01.git
```

Depois entre na pasta do projeto:

```bash
cd mini_projeto_01
```

**Esperado:** a pasta `mini_projeto_01` é criada com todos os arquivos.

---

## 🐍 Passo 2 — Criar o ambiente virtual

O ambiente virtual isola as dependências do projeto para não afetar outras coisas no seu computador.

```bash
python -m venv venv
```

**Esperado:** uma pasta `venv` é criada dentro do projeto.

---

## ✅ Passo 3 — Ativar o ambiente virtual

A forma de ativar depende do seu sistema operacional:

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
```

> ⚠️ **Se der erro de "execução de scripts desabilitada"**, rode uma vez:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> E responda **S** quando ele perguntar.

### Windows (CMD)

```cmd
venv\Scripts\activate.bat
```

### Linux / Mac

```bash
source venv/bin/activate
```

**Esperado:** o prompt do terminal passa a mostrar `(venv)` no começo:

```
(venv) C:\...\mini_projeto_01>
```

---

## 📦 Passo 4 — Instalar as dependências

Com o `(venv)` ativo, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

**Esperado:** o pip baixa e instala as bibliotecas `requests` e `beautifulsoup4`.

> 💡 **Se o `pip` não for reconhecido**, tente:
> ```bash
> python -m pip install -r requirements.txt
> ```

---

## ▶️ Passo 5 — Executar o programa

Ainda com o `(venv)` ativo, rode:

```bash
python scraper.py
```

**Esperado:** aparece o menu principal:

```
=============================================
   BUSCADOR DE CÉDULAS - LEILÕES BR
=============================================
   1 - Buscar cédulas
   0 - Sair
=============================================
   Escolha uma opção:
```

Aí é só seguir as instruções na tela para buscar cédulas.

---

## 🔄 Passo 6 — Sair do ambiente virtual

Quando terminar de usar, digite:

```bash
deactivate
```

O `(venv)` desaparece do prompt, indicando que você saiu do ambiente isolado.

---

## 📋 Resumo rápido (para colar de uma vez)

### Windows (PowerShell)
```powershell
git clone https://github.com/elieltonestudo-maker/mini_projeto_01.git
cd mini_projeto_01
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scraper.py
```

### Linux / Mac
```bash
git clone https://github.com/elieltonestudo-maker/mini_projeto_01.git
cd mini_projeto_01
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py
```

---

## ❓ Problemas comuns

### "python não é reconhecido como comando"

**Solução:** o Python não está no PATH do sistema. Reinstale o Python marcando **"Add Python to PATH"** durante a instalação.

Alternativa: use `py` em vez de `python` no Windows:
```bash
py scraper.py
```

### "pip não é reconhecido como comando"

**Solução:** use o módulo Python direto:
```bash
python -m pip install -r requirements.txt
```

### "Set-ExecutionPolicy" — erro no PowerShell

**Solução:** rode uma vez e responda **S**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### O programa não encontra as bibliotecas

**Solução:** confirme que o `(venv)` está ativo (aparece no prompt). Se não estiver, ative novamente:
```powershell
venv\Scripts\Activate.ps1
```

### Erro de conexão ao buscar no site

**Solução:** verifique sua conexão com a internet. Se o site estiver fora do ar, tente novamente em alguns minutos.

---

## 📚 Próximos passos

Depois que conseguir rodar, consulte o arquivo [**COMO_USAR.md**](COMO_USAR.md) para ver o roteiro de teste e as funcionalidades disponíveis.

---

## 🧑‍💻 Desenvolvedor

- **Nome:** Elielton Barbosa
- **Instituição:** Fatec Rio Claro
- **Disciplina:** Linguagem de Programação 2
- **Professor:** Orlando Saraiva Júnior