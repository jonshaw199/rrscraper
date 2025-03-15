from bs4 import BeautifulSoup
from ExportFormat import ExportFormat
from OP25Exporter import OP25Exporter
from os import mkdir
from requests import get
from time import time

exporters = {ExportFormat.OP25: OP25Exporter}


class Scraper:
    def __init__(self, url: str, outformat: ExportFormat = None, outdir: str = None):
        html = get(url).text
        self.soup = BeautifulSoup(html, "html.parser")
        self.exporter = exporters[outformat or ExportFormat.OP25]
        if not self.exporter:
            raise ValueError(f"Don't know how to handle format {outformat}")
        self.outdir = outdir or str(time())

    def scrape(self):
        mkdir(self.outdir)
