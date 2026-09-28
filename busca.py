# busca.py - Classe que representa uma busca no site Leilões BR
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
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


class Busca:
    """Representa uma busca de cédulas no site Leilões BR."""

    def __init__(self, pais):
        """Cria uma busca para o país informado."""
        self.pais = pais
        self.termo = f"{pais} cedula"
        self.filtros = {
            "ano": None,
            "pick": None,
            "estado": None,
            "leiloeiro": None,
            "data_limite": None,
        }
        self.lotes = []

    def adicionar_filtro(self, nome, valor):
        """Adiciona ou atualiza um filtro."""
        if nome in self.filtros:
            self.filtros[nome] = valor

    def limpar_filtros(self):
        """Limpa todos os filtros."""
        for chave in self.filtros:
            self.filtros[chave] = None

    def tem_filtro_ativo(self):
        """Devolve True se pelo menos um filtro estiver ativo."""
        return any(self.filtros.values())

    def executar(self):
        """Executa a busca completa: baixa, filtra cédulas, aplica filtros e ordena."""
        print(f"   Baixando resultados para: {self.termo}")

        self.lotes = self._baixar_todas_paginas()
        print(f"   Lotes encontrados no site: {len(self.lotes)}")

        self.lotes = self._filtrar_cedulas()
        print(f"   Lotes que são cédulas: {len(self.lotes)}")

        self.lotes = self._aplicar_filtros()
        self.lotes.sort(key=lambda l: l.data or datetime.max)
        print(f"   Lotes após os filtros: {len(self.lotes)}")

        return self.lotes

    def _baixar_pagina(self, pagina=1):
        """Baixa uma página de resultados."""
        parametros = {
            "op": "2",
            "pesquisa": self.termo,
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

    def _baixar_todas_paginas(self):
        """Baixa todas as páginas de resultados até não encontrar mais lotes."""
        todos_lotes = []
        pagina = 1

        while True:
            print(f"   Baixando página {pagina}...")
            html = self._baixar_pagina(pagina)

            if html is None:
                break

            sopa = BeautifulSoup(html, "html.parser")
            tags_lotes = sopa.find_all("div", class_="mostbidded")

            if not tags_lotes:
                break

            for tag in tags_lotes:
                todos_lotes.append(Lote(tag))

            pagina += 1

            if pagina > 20:
                print("   Limite de 20 páginas atingido.")
                break

        return todos_lotes

    def _filtrar_cedulas(self):
        """Deixa só os lotes cujo título menciona cédula."""
        palavras = ["cédula", "cedula", "cédulas", "cedulas"]
        filtrados = []
        for lote in self.lotes:
            if lote.titulo is None:
                continue
            titulo_minusculo = lote.titulo.lower()
            for palavra in palavras:
                if palavra in titulo_minusculo:
                    filtrados.append(lote)
                    break
        return filtrados

    def _aplicar_filtros(self):
        """Aplica todos os filtros ativos na lista de lotes."""
        if not self.tem_filtro_ativo():
            return self.lotes

        filtrados = []
        for lote in self.lotes:
            if lote.titulo is None:
                continue
            titulo_minusculo = lote.titulo.lower()
            passa = True

            if self.filtros["ano"]:
                if self.filtros["ano"] not in titulo_minusculo:
                    passa = False

            if self.filtros["pick"]:
                p = self.filtros["pick"]
                if p not in titulo_minusculo and f"p-{p}" not in titulo_minusculo:
                    passa = False

            if self.filtros["estado"]:
                padrao = PADROES_ESTADO.get(self.filtros["estado"])
                if not padrao or not re.search(padrao, lote.titulo, re.IGNORECASE):
                    passa = False

            if self.filtros["leiloeiro"]:
                if not lote.leiloeiro or self.filtros["leiloeiro"] not in lote.leiloeiro.lower():
                    passa = False

            if self.filtros["data_limite"]:
                limite = datetime.strptime(self.filtros["data_limite"], "%Y-%m-%d")
                if lote.data is None or lote.data > limite:
                    passa = False

            if passa:
                filtrados.append(lote)

        return filtrados

    def salvar_txt(self, nome_arquivo):
        """Salva os lotes em um arquivo de texto."""
        nome = nome_arquivo.strip()
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
        arquivo.write(f"País: {self.pais}\n")
        arquivo.write("Filtros aplicados:\n")

        algum_filtro = False
        for chave, valor in self.filtros.items():
            if valor:
                arquivo.write(f"  - {chave}: {valor}\n")
                algum_filtro = True
        if not algum_filtro:
            arquivo.write("  (nenhum)\n")

        agora = datetime.now().strftime("%d/%m/%Y %H:%M")
        arquivo.write(f"Total de lotes: {len(self.lotes)}\n")
        arquivo.write(f"Data da busca: {agora}\n")
        arquivo.write("=" * 45 + "\n\n")

        for i, lote in enumerate(self.lotes, start=1):
            arquivo.write(f"Lote {i}\n")
            arquivo.write(f"  Título:    {lote.titulo}\n")
            arquivo.write(f"  Preço:     {lote.preco}\n")
            arquivo.write(f"  Data:      {lote.data_formatada()}\n")
            arquivo.write(f"  Leiloeiro: {lote.leiloeiro}\n")
            arquivo.write(f"  Link:      {lote.link}\n\n")

        arquivo.close()
        print(f"   Arquivo salvo: {nome}")