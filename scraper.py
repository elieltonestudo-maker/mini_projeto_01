# mini_projeto_01 - Buscador de cédulas no site Leilões BR
# Este programa busca cédulas em leilões online usando web scraping.

# Configurações do site
ENDERECO_BUSCA = "https://leiloesbr.com.br/busca_andamento.asp"


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
    """Junta país e refinamento em um termo de busca só."""
    if refino == "ano":
        return f"{pais} {valor}"
    elif refino == "pick":
        return f"{pais} {valor}"
    elif refino == "estado":
        return f"{pais} {valor}"
    else:
        return pais


def buscar_cedulas():
    """Fluxo principal de busca (por enquanto só mostra o que seria buscado)."""
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
    print("   (busca ainda não implementada)")


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