# mini_projeto_01 - Buscador de cédulas no site Leilões BR
# Este programa busca cédulas em leilões online usando web scraping.

import requests
from bs4 import BeautifulSoup

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


def mostrar_menu_refino():
    """Mostra o menu de refinamento e devolve a opção escolhida."""
    print()
    print("   Como deseja refinar a busca?")
    print("   1 - Buscar por ano")
    print("   2 - Buscar por Pick (código internacional)")
    print("   3 - Buscar por estado de conservação")
    print("   4 - Buscar só pelo país")
    print("   0 - Voltar")
    print("-" * 45)
    return input("   Escolha uma opção: ")


def pedir_ano():
    """Pede o ano da cédula."""
    return input("   Digite o ano (ex: 1960): ").strip()


def pedir_pick():
    """Pede o número do Pick da cédula."""
    return input("   Digite o número do Pick (ex: 216): ").strip()


def mostrar_menu_estado():
    """Mostra as opções de estado de conservação."""
    print()
    print("   Estados disponíveis:")
    print("   1 - MBC (Muito Bem Conservada)")
    print("   2 - SOB / Soberba")
    print("   3 - FE / Flor de Estampa")
    print("   4 - BC (Bem Conservada)")
    print("   5 - Digitar outro")
    print("   0 - Voltar")
    print("-" * 45)
    return input("   Escolha uma opção: ")


def escolher_estado():
    """Traduz a opção do menu para o termo de busca."""
    opcao = mostrar_menu_estado()
    if opcao == "1":
        return "mbc"
    elif opcao == "2":
        return "sob"
    elif opcao == "3":
        return "fe"
    elif opcao == "4":
        return "bc"
    elif opcao == "5":
        return input("   Digite o estado: ").strip().lower()
    else:
        return None


def montar_termo_busca(pais, refino, valor):
    """Junta o país, a palavra 'cedula' e o refinamento em um termo de busca só."""
    # Sempre inclui "cedula" para o site filtrar melhor
    partes = [pais, "cedula"]

    if refino == "ano":
        partes.append(valor)
    elif refino == "pick":
        partes.append(valor)
    elif refino == "estado":
        partes.append(valor)
    # Se refino == "pais", não adiciona nada extra

    return " ".join(partes)


def baixar_pagina(termo):
    """Baixa a página de busca do site e devolve o HTML ou None se der erro."""
    # Parâmetros da URL: op=2 é a busca em andamento
    parametros = {
        "op": "2",
        "pesquisa": termo,
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

def buscar_cedulas():
    """Fluxo principal de busca."""
    pais = pedir_pais()
    if not pais:
        print("   País não informado. Voltando ao menu.")
        return

    opcao = mostrar_menu_refino()

    refino = None
    valor = None

    if opcao == "1":
        refino = "ano"
        valor = pedir_ano()
    elif opcao == "2":
        refino = "pick"
        valor = pedir_pick()
    elif opcao == "3":
        refino = "estado"
        valor = escolher_estado()
        if valor is None:
            print("   Voltando ao menu.")
            return
    elif opcao == "4":
        refino = "pais"
    else:
        print("   Voltando ao menu.")
        return

    termo = montar_termo_busca(pais, refino, valor)
    print()
    print("=" * 45)
    print(f"   Buscando por: {termo}")
    print("=" * 45)

    html = baixar_pagina(termo)

    if html is None:
        print("   Não foi possível baixar a página.")
        return

        print(f"   Página baixada com sucesso.")
    print(f"   Tamanho do HTML: {len(html)} caracteres.")
    print()

    lotes = encontrar_lotes(html)
    print(f"   Lotes encontrados no site: {len(lotes)}")

    lotes = filtrar_cedulas(lotes)
    print(f"   Lotes que são cédulas: {len(lotes)}")
    print()

    # Mostra o link dos 8 primeiros lotes
    print("   Links dos 8 primeiros lotes:")
    print("-" * 45)
    for lote in lotes[:8]:
        titulo = pegar_titulo(lote)
        link = pegar_link(lote)
        print(f"   Título: {titulo}")
        print(f"   Link:   {link}")
        print()


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