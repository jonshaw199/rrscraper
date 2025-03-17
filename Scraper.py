from bs4 import BeautifulSoup
from os import mkdir
from requests import get
from time import time


class Scraper:
    def __init__(self, url: str, outdir: str = None):
        html = get(url).text
        self.soup = BeautifulSoup(html, "html.parser")
        self.outdir = outdir or str(time())

    def scrape(self):
        mkdir(self.outdir)
