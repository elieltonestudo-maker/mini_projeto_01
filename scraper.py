# mini_projeto_01 - Buscador de cédulas no site Leilões BR
# Este programa busca cédulas em leilões online usando web scraping.

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from lote import Lote

# Configurações do site
ENDERECO_BUSCA = "https://leiloesbr.com.br/busca_andamento.asp"

# Cabeçalho para o site achar que somos um navegador de verdade
CABECALHO = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# Padrões de estado de conservação (usados com expressão regular)
PADROES_ESTADO = {
    "mbc": r"\bmbc\b",
    "sob": r"\bsob\b|\bsoberba\b",
    "fe": r"\bfe\b|\bflor de estampa\b",
    "bc": r"\bbc\b",
    "regular": r"\bregular\b",
}


def mostrar_menu_principal():
    """Mostra o menu inicial e devolve a opção escolhida."""
    print("=" * 45)
    print("   BUSCADOR DE CÉDULAS - LEILÕES BR")
    print("=" * 45)
    print("   1 - Buscar cédulas")
    print("   0 - Sair")
    print("=" * 45)
    return input("   Escolha uma opção: ")


def pedir_pais():
    """Pede o nome do país para o usuário."""
    print()
    pais = input("   Digite o país da cédula: ")
    return pais.strip().lower()


def pedir_ano():
    """Pede o ano da cédula."""
    return input("   Digite o ano (ex: 1960): ").strip()


def pedir_pick():
    """Pede o número do Pick da cédula."""
    return input("   Digite o número do Pick (ex: 216): ").strip()


def pedir_leiloeiro():
    """Pede o nome do leiloeiro."""
    return input("   Digite o nome do leiloeiro: ").strip().lower()


def pedir_data_limite():
    """Pede uma data limite no formato D/M/AAAA."""
    return input("   Mostrar lotes que encerram até (ex: 30/9/2026): ").strip()


def mostrar_menu_estado():
    """Mostra as opções de estado de conservação."""
    print()
    print("   Estados disponíveis:")
    print("   1 - FE / Flor de Estampa")
    print("   2 - SOB / Soberba")
    print("   3 - MBC (Muito Bem Conservada)")
    print("   4 - BC (Bem Conservada)")
    print("   5 - Digitar outro")
    print("   0 - Voltar")
    print("-" * 45)
    return input("   Escolha uma opção: ")


def escolher_estado():
    """Traduz a opção do menu para o termo de busca."""
    opcao = mostrar_menu_estado()
    if opcao == "1":
        return "fe"
    elif opcao == "2":
        return "sob"
    elif opcao == "3":
        return "mbc"
    elif opcao == "4":
        return "bc"
    elif opcao == "5":
        return input("   Digite o estado: ").strip().lower()
    else:
        return None


def converter_data(texto):
    """Tenta converter uma string em data. Aceita vários formatos.

    Retorna um objeto datetime ou None se nenhum formato funcionar.
    """
    formatos = [
        "%d/%m/%Y",   # 30/09/2026 ou 30/9/2026
        "%d/%m/%y",   # 30/09/26 ou 30/9/26
        "%Y-%m-%d",   # 2026-09-30
        "%d-%m-%Y",   # 30-09-2026
        "%d-%m-%y",   # 30-09-26
        "%d.%m.%Y",   # 30.09.2026
    ]
    for formato in formatos:
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            continue
    return None


def mostrar_resumo_filtros(pais, filtros):
    """Mostra o cabeçalho com o país e os filtros ativos no momento."""
    print()
    print("=" * 45)
    print(f"   País: {pais}")

    ativos = []
    if filtros["ano"]:
        ativos.append(f"   - ano: {filtros['ano']}")
    if filtros["pick"]:
        ativos.append(f"   - pick: {filtros['pick']}")
    if filtros["estado"]:
        ativos.append(f"   - estado: {filtros['estado']}")
    if filtros["leiloeiro"]:
        ativos.append(f"   - leiloeiro: {filtros['leiloeiro']}")
    if filtros["data_limite"]:
        ativos.append(f"   - data limite: {filtros['data_limite']}")

    if ativos:
        print("   Filtros ativos:")
        for linha in ativos:
            print(linha)
    else:
        print("   Filtros ativos: (nenhum)")

    print()
    print("   1 - Adicionar filtro de ano")
    print("   2 - Adicionar filtro de Pick")
    print("   3 - Adicionar filtro de estado de conservação")
    print("   4 - Adicionar filtro de leiloeiro")
    print("   5 - Adicionar filtro de data limite")
    print("   6 - Buscar agora")
    print("   7 - Limpar filtros")
    print("   0 - Voltar ao menu principal")
    print("=" * 45)


def escolher_filtros(pais):
    """Menu combinável de filtros. Roda até o usuário mandar buscar.

    Retorna um dicionário com os filtros escolhidos, ou None se o
    usuário quiser voltar ao menu principal sem buscar.
    """
    filtros = {
        "ano": None,
        "pick": None,
        "estado": None,
        "leiloeiro": None,
        "data_limite": None,
    }

    while True:
        mostrar_resumo_filtros(pais, filtros)
        opcao = input("   Escolha uma opção: ")

        if opcao == "1":
            valor = pedir_ano()
            if valor:
                filtros["ano"] = valor
                print(f"   Filtro de ano adicionado: {valor}")
        elif opcao == "2":
            valor = pedir_pick()
            if valor:
                filtros["pick"] = valor
                print(f"   Filtro de Pick adicionado: {valor}")
        elif opcao == "3":
            estado = escolher_estado()
            if estado:
                filtros["estado"] = estado
                print(f"   Filtro de estado adicionado: {estado}")
        elif opcao == "4":
            valor = pedir_leiloeiro()
            if valor:
                filtros["leiloeiro"] = valor
                print(f"   Filtro de leiloeiro adicionado: {valor}")
        elif opcao == "5":
            valor = pedir_data_limite()
            if valor:
                data_convertida = converter_data(valor)
                if data_convertida is None:
                    print(f"   Data inválida: {valor}")
                    print("   Formatos aceitos: 30/9/2026, 30/09/2026, 2026-09-30")
                else:
                    filtros["data_limite"] = data_convertida.strftime("%Y-%m-%d")
                    print(f"   Filtro de data limite adicionado: {valor}")
        elif opcao == "6":
            return filtros
        elif opcao == "7":
            for chave in filtros:
                filtros[chave] = None
            print("   Filtros limpos.")
        elif opcao == "0":
            return None
        else:
            print("   Opção inválida.")


def montar_termo_busca(pais):
    """Junta o país com a palavra 'cedula' para a busca no site."""
    return f"{pais} cedula"


def baixar_pagina(termo, pagina=1):
    """Baixa a página de busca do site e devolve o HTML ou None se der erro."""
    parametros = {
        "op": "2",
        "pesquisa": termo,
        "v": "21",
        "pag": str(pagina),
    }

    try:
        resposta = requests.get(
            ENDERECO_BUSCA,
            params=parametros,
            headers=CABECALHO,
            timeout=30,
        )
        resposta.raise_for_status()
        return resposta.text
    except requests.RequestException as erro:
        print(f"   Erro ao baixar a página: {erro}")
        return None


def encontrar_lotes(html):
    """Recebe o HTML da página e devolve uma lista com as tags de cada lote."""
    sopa = BeautifulSoup(html, "html.parser")
    lotes = sopa.find_all("div", class_="mostbidded")
    return lotes


def baixar_todas_paginas(termo):
    """Baixa todas as páginas de resultados até não encontrar mais lotes."""
    todos_lotes = []
    pagina = 1

    while True:
        print(f"   Baixando página {pagina}...")
        html = baixar_pagina(termo, pagina)

        if html is None:
            break

        tags_lotes = encontrar_lotes(html)

        if not tags_lotes:
            break

        # Converte cada tag HTML em um objeto Lote
        for tag in tags_lotes:
            todos_lotes.append(Lote(tag))

        pagina += 1

        if pagina > 20:
            print("   Limite de 20 páginas atingido.")
            break

    return todos_lotes


def filtrar_cedulas(lotes):
    """Filtra a lista, deixando só os lotes cujo título menciona cédula."""
    palavras = ["cédula", "cedula", "cédulas", "cedulas"]
    filtrados = []
    for lote in lotes:
        if lote.titulo is None:
            continue
        titulo_minusculo = lote.titulo.lower()
        for palavra in palavras:
            if palavra in titulo_minusculo:
                filtrados.append(lote)
                break
    return filtrados


def aplicar_filtros(lotes, filtros):
    """Aplica todos os filtros ativos na lista de lotes."""
    if not any(filtros.values()):
        return lotes

    filtrados = []
    for lote in lotes:
        if lote.titulo is None:
            continue
        titulo_minusculo = lote.titulo.lower()

        passa = True

        if filtros["ano"]:
            if filtros["ano"] not in titulo_minusculo:
                passa = False

        if filtros["pick"]:
            p = filtros["pick"]
            if p not in titulo_minusculo and f"p-{p}" not in titulo_minusculo:
                passa = False

        if filtros["estado"]:
            padrao = PADROES_ESTADO.get(filtros["estado"])
            if not padrao or not re.search(padrao, lote.titulo, re.IGNORECASE):
                passa = False

        if filtros["leiloeiro"]:
            if not lote.leiloeiro or filtros["leiloeiro"] not in lote.leiloeiro.lower():
                passa = False

        if filtros["data_limite"]:
            limite = datetime.strptime(filtros["data_limite"], "%Y-%m-%d")
            if lote.data is None or lote.data > limite:
                passa = False

        if passa:
            filtrados.append(lote)

    return filtrados


def salvar_txt(lotes, pais, filtros):
    """Salva a lista de lotes em um arquivo de texto."""
    nome = input("   Digite o nome do arquivo (sem .txt): ").strip()
    if not nome:
        print("   Nome vazio. Salvamento cancelado.")
        return

    if not nome.endswith(".txt"):
        nome = nome + ".txt"

    try:
        arquivo = open(nome, "w", encoding="utf-8")
    except OSError as erro:
        print(f"   Erro ao criar o arquivo: {erro}")
        return

    arquivo.write("=" * 45 + "\n")
    arquivo.write("  BUSCADOR DE CÉDULAS - LEILÕES BR\n")
    arquivo.write("=" * 45 + "\n")
    arquivo.write(f"País: {pais}\n")
    arquivo.write("Filtros aplicados:\n")

    algum_filtro = False
    for chave, valor in filtros.items():
        if valor:
            arquivo.write(f"  - {chave}: {valor}\n")
            algum_filtro = True
    if not algum_filtro:
        arquivo.write("  (nenhum)\n")

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    arquivo.write(f"Total de lotes: {len(lotes)}\n")
    arquivo.write(f"Data da busca: {agora}\n")
    arquivo.write("=" * 45 + "\n\n")

    for i, lote in enumerate(lotes, start=1):
        arquivo.write(f"Lote {i}\n")
        arquivo.write(f"  Título:    {lote.titulo}\n")
        arquivo.write(f"  Preço:     {lote.preco}\n")
        arquivo.write(f"  Data:      {lote.data_formatada()}\n")
        arquivo.write(f"  Leiloeiro: {lote.leiloeiro}\n")
        arquivo.write(f"  Link:      {lote.link}\n\n")

    arquivo.close()
    print(f"   Arquivo salvo: {nome}")


def mostrar_resultados(lotes, pais, filtros):
    """Mostra os lotes no terminal, de 8 em 8."""
    total = len(lotes)
    inicio = 0
    tamanho_bloco = 8
    ja_salvou = False

    while inicio < total:
        fim = min(inicio + tamanho_bloco, total)

        print(f"   Mostrando {inicio + 1}-{fim} de {total} lotes:")
        print("-" * 45)

        for lote in lotes[inicio:fim]:
            print(f"   Título:    {lote.titulo}")
            print(f"   Preço:     {lote.preco}")
            print(f"   Data:      {lote.data_formatada()}")
            print(f"   Leiloeiro: {lote.leiloeiro}")
            print(f"   Link:      {lote.link}")
            print()

        if fim < total:
            print("-" * 45)
            print("   [Enter] Próximos 8  |  [t] Mostrar todos  |  [s] Salvar em TXT  |  [q] Parar")
            escolha = input("   Opção: ").strip().lower()

            if escolha == "q":
                print("   Listagem encerrada.")
                return
            elif escolha == "t":
                tamanho_bloco = total - inicio
            elif escolha == "s":
                salvar_txt(lotes, pais, filtros)
                ja_salvou = True
        else:
            print("-" * 45)
            print("   Fim da lista.")
            print()
            if not ja_salvou:
                print("   Deseja salvar em TXT? (s/n): ", end="")
                if input().strip().lower() == "s":
                    salvar_txt(lotes, pais, filtros)
            return

        inicio = fim


def buscar_cedulas():
    """Fluxo principal de busca."""
    pais = pedir_pais()
    if not pais:
        print("   País não informado. Voltando ao menu.")
        return

    filtros = escolher_filtros(pais)
    if filtros is None:
        print("   Busca cancelada.")
        return

    termo = montar_termo_busca(pais)
    print()
    print("=" * 45)
    print(f"   Buscando por: {termo}")
    print("=" * 45)

    lotes = baixar_todas_paginas(termo)

    if not lotes:
        print("   Não foi possível baixar as páginas.")
        return

    print()
    print(f"   Lotes encontrados no site: {len(lotes)}")

    lotes = filtrar_cedulas(lotes)
    print(f"   Lotes que são cédulas: {len(lotes)}")

    lotes = aplicar_filtros(lotes, filtros)

    # Ordena por data (crescente)
    lotes.sort(key=lambda l: l.data or datetime.max)

    print(f"   Lotes após os filtros: {len(lotes)}")
    print()

    if not lotes:
        print("   Nenhum lote encontrado com esses critérios.")
        print()
        return

    mostrar_resultados(lotes, pais, filtros)


def main():
    """Função principal que roda o programa."""
    while True:
        opcao = mostrar_menu_principal()

        if opcao == "1":
            buscar_cedulas()
        elif opcao == "0":
            print()
            print("   Até logo!")
            break
        else:
            print()
            print("   Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()