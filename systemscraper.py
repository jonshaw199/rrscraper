from bs4 import BeautifulSoup, Tag
import csv
import os
import requests
from typing import List

from scraper import Scraper

base_url = "https://www.radioreference.com"


class SystemScraper(Scraper):
    def __init__(self, url: str, out_dir: str = None):
        super().__init__(url, out_dir)

    def scrape(self):
        super().scrape()
        self._export_details()
        self._export_sites_and_freqs()
        os.mkdir(f"{self.out_dir}/talkgroups")
        self._export_talkgroups()

    def _export_details(self):
        with open(f"{self.out_dir}/details.csv", "w") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(
                [
                    "System Name",
                    "Location",
                    "County",
                    "System Type",
                    "System Voice",
                    "System ID",
                ]
            )
            csvwriter.writerow(
                [
                    self._get_detail_by_label("System Name:"),
                    self._get_detail_by_label("Location:"),
                    self._get_detail_by_label("County:"),
                    self._get_detail_by_label("System Type:"),
                    self._get_detail_by_label("System Voice:"),
                    self._get_detail_by_label("System ID:"),
                ]
            )

    def _get_detail_by_label(self, label: str, soup: BeautifulSoup = None) -> str:
        return (soup or self.soup).find("th", string=label).find_next("td").text.strip()

    def _export_sites_and_freqs(self):
        header = self.soup.find("h3", string="Sites and Frequencies")
        table = header.find_next("table")
        rows = table.find_all("tr")
        with open(f"{self.out_dir}/sites_and_freqs.csv", "w") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(["RFSS", "Site", "Name", "County", "Freqs", "NAC"])
            last_row = None
            for tr in rows[1:]:
                cells = tr.find_all("td")
                is_new_row = bool(cells[0].text.strip())
                if is_new_row:
                    if last_row:
                        csvwriter.writerow(last_row)
                    last_row = [
                        cells[0].text.strip(),
                        cells[1].text.strip(),
                        cells[2].text.strip(),
                        cells[3].text.strip(),
                        self._get_freqs_str(cells[4:]),
                        self._get_nac_from_site_link(cells[2]),
                    ]
                else:
                    freqs_str = self._get_freqs_str(cells[4:])
                    last_row[4] += f",{freqs_str}"
            csvwriter.writerow(last_row)

    def _get_nac_from_site_link(self, cell: Tag):
        link_tag = cell.find("a")
        url = f"{base_url}{link_tag['href']}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        return self._get_detail_by_label("NAC:", soup)

    def _get_freqs_str(self, tags: List[Tag]):
        texts = map(lambda tag: tag.text.strip(), tags)
        filtered_texts = filter(lambda text: bool(text), texts)
        return ",".join(filtered_texts)

    def _export_talkgroups(self):
        header = self.soup.find("h3", string="Talkgroups")
        talkgroups_section = header.find_next("div", id="talkgroups")
        headers = talkgroups_section.find_all("h5")
        for header in headers:
            header_text = self._get_text_from_tag(header)
            table = header.find_next("table")
            rows = table.find_all("tr")
            with open(
                f"{self.out_dir}/talkgroups/{to_filename(header_text)}.csv", "w"
            ) as file:
                csvwriter = csv.writer(file)
                csvwriter.writerow(
                    ["DEC", "HEX", "Mode", "Alpha Tag", "Description", "Tag"]
                )
                for tr in rows[1:]:
                    cells = tr.find_all("td")
                    cell_vals = map(lambda cell: cell.text.strip(), cells)
                    csvwriter.writerow(cell_vals)

    def _get_text_from_tag(self, tag: Tag) -> str:
        return tag.find(text=True, recursive=False).strip()


def to_filename(text: str) -> str:
    return "".join(x for x in text if x.isalnum())
