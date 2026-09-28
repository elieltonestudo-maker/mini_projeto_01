# Como Usar e Testar o Buscador de Cédulas 🧪

Este documento traz um roteiro passo a passo para testar todas as funcionalidades do sistema. Siga na ordem sugerida para comprovar o funcionamento das classes e dos filtros.

---

## 🎯 Roteiro Sugerido para Teste e Validação

### 1. Busca simples (só pelo país)

**Objetivo:** Confirmar que o programa baixa todas as páginas e encontra os lotes.

- Execute o programa:
  ```bash
  python scraper.py
  ```
- Escolha a opção `1` (Buscar cédulas)
- Digite o país: `argentina`
- Escolha a opção `6` (Buscar agora) — sem adicionar filtros
- **Esperado:** o programa baixa 5 páginas e encontra cerca de **76 lotes**

### 2. Filtro por estado de conservação

**Objetivo:** Verificar que o filtro de estado funciona corretamente.

- País: `argentina`
- Adicione filtro `3` (estado de conservação)
- Escolha a opção `1` (FE / Flor de Estampa)
- Escolha `6` (Buscar agora)
- **Esperado:** só aparecem lotes com "FE" ou "Flor de Estampa" no título

### 3. Filtros combinados

**Objetivo:** Testar a combinação de vários filtros ao mesmo tempo.

- País: `argentina`
- Adicione filtro `4` (leiloeiro): `ana aquino`
- Adicione filtro `5` (data limite): `12/10/26`
- Escolha `6` (Buscar agora)
- **Esperado:** só aparecem lotes da **Ana Aquino Leilões** que encerram até **12/10/2026**

### 4. Salvar resultados em TXT

**Objetivo:** Confirmar que o arquivo é gerado corretamente.

- Após qualquer busca, navegue até o final da lista (ou use `t` para mostrar todos)
- Digite `s` na pergunta "Deseja salvar em TXT?"
- Informe um nome de arquivo (ex: `resultado_argentina`)
- **Esperado:** é criado um arquivo `.txt` com:
  - Cabeçalho (país, filtros, total, data da busca)
  - Cada lote numerado (`Lote 1`, `Lote 2`, ...)
  - Campos: Título, Preço, Data, Leiloeiro, Link

### 5. Testar data em formato alternativo

**Objetivo:** Verificar a flexibilidade do filtro de data.

- País: `argentina`
- Adicione filtro `5` (data limite)
- Digite a data no formato `30/09/26` (dois dígitos)
- **Esperado:** o sistema aceita e converte internamente para `2026-09-30`

---

## 🧭 Navegação durante a listagem

Quando os resultados aparecem, você pode:

| Tecla | Ação |
|-------|------|
| **Enter** | Mostrar os próximos 8 lotes |
| **t** | Mostrar todos os lotes restantes de uma vez |
| **s** | Salvar todos os lotes em um arquivo `.txt` |
| **q** | Parar a listagem e voltar ao menu principal |

---

## 📌 Menu de filtros

| Opção | Filtro |
|-------|--------|
| **1** | Adicionar filtro de ano |
| **2** | Adicionar filtro de Pick (código internacional) |
| **3** | Adicionar filtro de estado de conservação |
| **4** | Adicionar filtro de leiloeiro |
| **5** | Adicionar filtro de data limite |
| **6** | Buscar agora |
| **7** | Limpar todos os filtros |
| **0** | Voltar ao menu principal |

---

## 📋 Estados de conservação disponíveis

| Opção | Sigla | Significado |
|-------|-------|-------------|
| **1** | FE | Flor de Estampa (nunca circulou) |
| **2** | SOB | Soberba (quase perfeita) |
| **3** | MBC | Muito Bem Conservada |
| **4** | BC | Bem Conservada |
| **5** | (outro) | Digitar manualmente |

---

## 📅 Formatos de data aceitos

O filtro de data limite aceita vários formatos:

| Formato | Exemplo |
|---------|---------|
| DD/MM/AAAA | `30/09/2026` |
| D/M/AAAA | `30/9/2026` |
| DD/MM/AA | `30/09/26` |
| AAAA-MM-DD | `2026-09-30` |
| DD-MM-AAAA | `30-09-2026` |
| DD.MM.AAAA | `30.09.2026` |

---

## 💡 Dicas

- Os filtros **se combinam** — você pode adicionar vários antes de buscar.
- Se errar um filtro, use a opção `7` para limpar tudo e começar de novo.
- O programa **avisa** quando a data digitada é inválida e não adiciona o filtro.
- Se nenhum lote for encontrado, o programa mostra uma mensagem clara.
- A ordenação é sempre **crescente por data** — os leilões que encerram primeiro aparecem no topo.