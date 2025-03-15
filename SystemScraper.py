from os import mkdir
from Scraper import Scraper


class SystemScraper(Scraper):
    def __init__(self, url: str, outdir: str = None):
        super().__init__(url, outdir)

    def scrape(self):
        super().scrape()

    def _get_detail_by_label(self, label: str) -> str:
        return self.soup.find(string="System Name:").find_next("td").text.strip()

    def _export_sites_and_freqs(self):
        header = self.soup.find(string="Sites and Frequencies")
