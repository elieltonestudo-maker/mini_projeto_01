# fatec_rc-lp2-mini-projeto-01 - Buscador de cédulas no site Leilões BR
# Este programa busca cédulas em leilões online usando web scraping.

from datetime import datetime
from busca import Busca


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

def pedir_palavra_chave():
    """Pede uma palavra-chave livre para o usuário."""
    return input("   Digite a palavra-chave: ").strip().lower()

def pedir_faixa_preco():
    """Pede o preço mínimo e máximo. Repete até a faixa ser válida."""
    while True:
        minimo_texto = input("   Digite o preço mínimo (ou Enter para ignorar): ").strip()
        maximo_texto = input("   Digite o preço máximo (ou Enter para ignorar): ").strip()

        minimo = None
        maximo = None

        if minimo_texto:
            minimo = converter_preco(minimo_texto)
            if minimo is None:
                print(f"   Preço mínimo inválido: {minimo_texto}")
                print("   Tente novamente.")
                continue

        if maximo_texto:
            maximo = converter_preco(maximo_texto)
            if maximo is None:
                print(f"   Preço máximo inválido: {maximo_texto}")
                print("   Tente novamente.")
                continue

        # Validação: mínimo não pode ser maior que o máximo
        if minimo is not None and maximo is not None and minimo > maximo:
            print(f"   Erro: preço mínimo (R$ {minimo:.2f}) é maior que o máximo (R$ {maximo:.2f}).")
            print("   Tente novamente.")
            continue

        # Se chegou até aqui, a faixa é válida
        return minimo, maximo

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

def converter_preco(texto):
    """Converte texto de preço ('10', '10.50', 'R$ 10,00') em float ou None."""
    if not texto:
        return None
    limpo = texto.replace("R$", "").strip()
    limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
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
    if filtros["palavra_chave"]:
        ativos.append(f"   - palavra-chave: {filtros['palavra_chave']}")
    if filtros["preco_min"] is not None or filtros["preco_max"] is not None:
        minimo = filtros["preco_min"]
        maximo = filtros["preco_max"]
        if minimo is not None and maximo is not None:
            ativos.append(f"   - preço: R$ {minimo:.2f} até R$ {maximo:.2f}")
        elif minimo is not None:
            ativos.append(f"   - preço: a partir de R$ {minimo:.2f}")
        else:
            ativos.append(f"   - preço: até R$ {maximo:.2f}")

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
    print("   6 - Adicionar palavra-chave")
    print("   7 - Adicionar faixa de preço")
    print("   8 - Buscar agora")
    print("   9 - Limpar filtros")
    print("   0 - Voltar ao menu principal")
    print("=" * 45)

def escolher_filtros(pais):
    """Menu combinável de filtros. Devolve um dicionário ou None se cancelar."""
    filtros = {
        "ano": None,
        "pick": None,
        "estado": None,
        "leiloeiro": None,
        "data_limite": None,
        "palavra_chave": None,
        "preco_min": None,
        "preco_max": None,
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
            valor = pedir_palavra_chave()
            if valor:
                filtros["palavra_chave"] = valor
                print(f"   Palavra-chave adicionada: {valor}")
        elif opcao == "7":
            minimo, maximo = pedir_faixa_preco()
            if minimo is not None or maximo is not None:
                filtros["preco_min"] = minimo
                filtros["preco_max"] = maximo
                print("   Faixa de preço adicionada.")
        elif opcao == "8":
            return filtros
        elif opcao == "9":
            for chave in filtros:
                filtros[chave] = None
            print("   Filtros limpos.")
        elif opcao == "0":
            return None
        else:
            print("   Opção inválida.")

def mostrar_resultados(lotes, busca):
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
                nome = input("   Digite o nome do arquivo (sem .txt): ")
                busca.salvar_txt(nome)
                ja_salvou = True
        else:
            print("-" * 45)
            print("   Fim da lista.")
            print()
            if not ja_salvou:
                print("   Deseja salvar em TXT? (s/n): ", end="")
                if input().strip().lower() == "s":
                    nome = input("   Digite o nome do arquivo (sem .txt): ")
                    busca.salvar_txt(nome)
            return

        inicio = fim


def buscar_cedulas():
    """Fluxo principal de busca usando a classe Busca."""
    pais = pedir_pais()
    if not pais:
        print("   País não informado. Voltando ao menu.")
        return

    filtros_escolhidos = escolher_filtros(pais)
    if filtros_escolhidos is None:
        print("   Busca cancelada.")
        return

    # Cria o objeto Busca e passa os filtros escolhidos
    busca = Busca(pais)
    for chave, valor in filtros_escolhidos.items():
        if valor is not None:
            busca.adicionar_filtro(chave, valor)

    print()
    print("=" * 45)
    print(f"   Buscando por: {busca.termo}")
    print("=" * 45)

    lotes = busca.executar()
    print()

    if not lotes:
        print("   Nenhum lote encontrado com esses critérios.")
        print()
        return

    mostrar_resultados(lotes, busca)


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