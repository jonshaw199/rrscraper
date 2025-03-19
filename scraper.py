import bs4
import os
import requests
import time


class Scraper:
    def __init__(self, url: str, out_dir: str = None):
        html = requests.get(url).text
        self.soup = bs4.BeautifulSoup(html, "html.parser")
        self.out_dir = f"data/{out_dir or str(time.time())}"

    def scrape(self):
        os.makedirs(self.out_dir, exist_ok=True)
