import bs4
from datetime import datetime
import os
import requests
import time


class Scraper:
    def __init__(self, url: str, out_dir: str = None):
        html = requests.get(url).text
        self._soup = bs4.BeautifulSoup(html, "html.parser")
        self._out_dir = f"data/{out_dir or datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def scrape(self):
        os.makedirs(self._out_dir, exist_ok=True)

    @property
    def out_dir(self):
        return self._out_dir

    def _get_text_from_tag(self, tag: bs4.Tag | None) -> str:
        if not tag:
            return ""

        shallow_text = tag.find(text=True, recursive=False)
        if shallow_text:
            return shallow_text.strip()

        # No shallow text — fall back to all text (deep)
        deep_text = tag.get_text(strip=True)
        return deep_text
