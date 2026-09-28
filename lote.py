# lote.py - Classe que representa um lote de cédula encontrado no site
from datetime import datetime


class Lote:
    """Representa um lote de cédula do site Leilões BR."""

    def __init__(self, tag_html):
        """Recebe a tag HTML do lote e extrai todos os dados."""
        self.titulo = self._pegar_titulo(tag_html)
        self.preco = self._pegar_preco(tag_html)
        self.data = self._pegar_data(tag_html)
        self.leiloeiro = self._pegar_leiloeiro(tag_html)
        self.link = self._pegar_link(tag_html)

    def _pegar_titulo(self, tag_html):
        """Pega o título completo do lote."""
        tag_titulo = tag_html.find("div", class_="mostbidded__title")
        if tag_titulo is None:
            return None
        tag_a = tag_titulo.find("a")
        if tag_a is None:
            return None
        return tag_a.get("data-bs-original-title") or tag_a.get_text(strip=True)

    def _pegar_preco(self, tag_html):
        """Pega o preço do lote."""
        tag_preco = tag_html.find("div", class_="venda-price")
        if tag_preco is None:
            return None
        return tag_preco.get_text(strip=True)

    def _pegar_data(self, tag_html):
        """Pega a data de encerramento como objeto datetime."""
        infos = tag_html.find_all("div", class_="mostbidded__info")
        if not infos:
            return None
        texto = infos[0].get_text(strip=True)
        parte_data = texto.split("-")[0].strip()
        try:
            return datetime.strptime(parte_data, "%d/%m/%Y")
        except ValueError:
            return None

    def _pegar_leiloeiro(self, tag_html):
        """Pega o nome do leiloeiro."""
        infos = tag_html.find_all("div", class_="mostbidded__info")
        if not infos:
            return None
        tag_leiloeiro = infos[-1].find("a")
        if tag_leiloeiro is None:
            return infos[-1].get_text(strip=True)
        return tag_leiloeiro.get_text(strip=True)

    def _pegar_link(self, tag_html):
        """Pega o link do lote como URL completa."""
        tag_link = tag_html.find("a", class_="stretched-link")
        if tag_link is None:
            return None
        href = tag_link.get("href", "")
        if href.startswith("http"):
            return href
        return "https://leiloesbr.com.br/" + href

    def data_formatada(self):
        """Devolve a data formatada como string (DD/MM/AAAA) ou '(sem data)'."""
        if self.data:
            return self.data.strftime("%d/%m/%Y")
        return "(sem data)"