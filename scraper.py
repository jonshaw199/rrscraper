import bs4
import os
import requests
import time


class Scraper:
    def __init__(self, url: str, outdir: str = None):
        html = requests.get(url).text
        self.soup = bs4.BeautifulSoup(html, "html.parser")
        self.outdir = f"data/{outdir or str(time.time())}"

    def scrape(self):
        os.makedirs(self.outdir, exist_ok=True)
