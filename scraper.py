# mini_projeto_01 - Buscador de cédulas no site Leilões BR
# Este programa busca cédulas em leilões online usando web scraping.

import requests
from bs4 import BeautifulSoup
import re

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
    print("   5 - Buscar agora")
    print("   6 - Limpar filtros")
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
            return filtros
        elif opcao == "6":
            for chave in filtros:
                filtros[chave] = None
            print("   Filtros limpos.")
        elif opcao == "0":
            return None
        else:
            print("   Opção inválida.")


def aplicar_filtros(lotes, filtros):
    """Aplica todos os filtros ativos na lista de lotes."""
    # Se todos os filtros forem None, devolve a lista inteira
    if not any(filtros.values()):
        return lotes

    filtrados = []
    for lote in lotes:
        titulo = pegar_titulo(lote)
        leiloeiro = pegar_leiloeiro(lote)
        if titulo is None:
            continue
        titulo_minusculo = titulo.lower()

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
            if not padrao or not re.search(padrao, titulo, re.IGNORECASE):
                passa = False

        if filtros["leiloeiro"]:
            if not leiloeiro or filtros["leiloeiro"] not in leiloeiro.lower():
                passa = False

        if passa:
            filtrados.append(lote)

    return filtrados


def montar_termo_busca(pais):
    """Junta o país com a palavra 'cedula' para a busca no site."""
    return f"{pais} cedula"

    return " ".join(partes)


def baixar_pagina(termo, pagina=1):
    """Baixa a página de busca do site e devolve o HTML ou None se der erro."""
    parametros = {
        "op": "2",
        "pesquisa": termo,
        "v": "21",       # <-- força 21 itens por página (ativa paginação)
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
    """Recebe o HTML da página e devolve uma lista com os blocos de cada lote."""
    sopa = BeautifulSoup(html, "html.parser")
    # Cada lote fica dentro de uma <div class="mostbidded ...">
    lotes = sopa.find_all("div", class_="mostbidded")
    return lotes

def pegar_link(lote):
    """Pega o link do lote e devolve a URL completa."""
    # O link fica dentro de <a> com classe 'stretched-link'
    tag_link = lote.find("a", class_="stretched-link")
    if tag_link is None:
        return None
    # O href é relativo, então juntamos com o endereço do site
    href = tag_link.get("href", "")
    if href.startswith("http"):
        return href
    return "https://leiloesbr.com.br/" + href

def pegar_titulo(lote):
    """Pega o título completo do lote (usando o atributo data-bs-original-title)."""
    # O título completo fica no atributo data-bs-original-title do <a> dentro do título
    tag_titulo = lote.find("div", class_="mostbidded__title")
    if tag_titulo is None:
        return None
    tag_a = tag_titulo.find("a")
    if tag_a is None:
        return None
    # Tenta pegar o atributo completo; se não tiver, usa o texto do <h3>
    titulo = tag_a.get("data-bs-original-title") or tag_a.get_text(strip=True)
    return titulo

def pegar_preco(lote):
    """Pega o preço do lote."""
    tag_preco = lote.find("div", class_="venda-price")
    if tag_preco is None:
        return None
    return tag_preco.get_text(strip=True)

def pegar_leiloeiro(lote):
    """Pega o nome do leiloeiro do lote."""
    # As infos ficam em <div class="mostbidded__info ...">, e a última é o leiloeiro
    infos = lote.find_all("div", class_="mostbidded__info")
    if not infos:
        return None
    # A última div de info é o leiloeiro (a primeira é data/UF)
    tag_leiloeiro = infos[-1].find("a")
    if tag_leiloeiro is None:
        return infos[-1].get_text(strip=True)
    return tag_leiloeiro.get_text(strip=True)

def filtrar_cedulas(lotes):
    """Filtra a lista, deixando só os lotes cujo título menciona cédula."""
    # Variações aceitas (com e sem acento, singular e plural)
    palavras = ["cédula", "cedula", "cédulas", "cedulas"]
    filtrados = []
    for lote in lotes:
        titulo = pegar_titulo(lote)
        if titulo is None:
            continue
        titulo_minusculo = titulo.lower()
        for palavra in palavras:
            if palavra in titulo_minusculo:
                filtrados.append(lote)
                break
    return filtrados



def baixar_todas_paginas(termo):
    """Baixa todas as páginas de resultados até não encontrar mais lotes."""
    todos_lotes = []
    pagina = 1

    while True:
        print(f"   Baixando página {pagina}...")
        html = baixar_pagina(termo, pagina)

        if html is None:
            break

        lotes = encontrar_lotes(html)

        if not lotes:
            # Página vazia: acabaram os resultados
            break

        todos_lotes.extend(lotes)
        pagina += 1

        # Segurança: para depois de 20 páginas
        if pagina > 20:
            print("   Limite de 20 páginas atingido.")
            break

    return todos_lotes

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
    print(f"   Lotes após os filtros: {len(lotes)}")
    print()

    if not lotes:
        print("   Nenhum lote encontrado com esses critérios.")
        print()
        return

    # Mostra os resultados (até 8 por vez)
    mostrar_resultados(lotes)


def mostrar_resultados(lotes):
    """Mostra os lotes no terminal, de 8 em 8."""
    total = len(lotes)
    inicio = 0
    tamanho_bloco = 8

    while inicio < total:
        fim = min(inicio + tamanho_bloco, total)

        print(f"   Mostrando {inicio + 1}-{fim} de {total} lotes:")
        print("-" * 45)

        for lote in lotes[inicio:fim]:
            titulo = pegar_titulo(lote)
            preco = pegar_preco(lote)
            leiloeiro = pegar_leiloeiro(lote)
            link = pegar_link(lote)
            print(f"   Título:    {titulo}")
            print(f"   Preço:     {preco}")
            print(f"   Leiloeiro: {leiloeiro}")
            print(f"   Link:      {link}")
            print()

        # Se ainda tem mais lotes, pergunta o que fazer
        if fim < total:
            print("-" * 45)
            print("   [Enter] Próximos 8  |  [t] Mostrar todos  |  [q] Parar")
            escolha = input("   Opção: ").strip().lower()

            if escolha == "q":
                print("   Listagem encerrada.")
                return
            elif escolha == "t":
                tamanho_bloco = total - inicio  # mostra todo o resto de uma vez
            # Se for Enter (vazio), continua com o bloco normal
        else:
            print("-" * 45)
            print("   Fim da lista.")
            print()

        inicio = fim

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