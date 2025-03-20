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
        th_tag = (soup or self.soup).find("th", string=label)
        if th_tag:
            td_tag = th_tag.find_next("td")
            return td_tag.text.strip() if td_tag else ""
        return ""

    def _export_sites_and_freqs(self):
        header = self.soup.find("h3", string="Sites and Frequencies")
        table = header.find_next("table")
        rows = table.find_all("tr")
        header_items = rows[0].find_all('th')

        # Map column names to their indices
        column_indices = {}
        for idx, th in enumerate(header_items):
            column_name = th.text.strip()
            if column_name:
                column_indices[column_name] = idx

        # Open CSV file for writing
        with open(f"{self.out_dir}/sites_and_freqs.csv", "w") as file:
            csvwriter = csv.writer(file)

            # Write the header row, including "NAC"
            header_texts = [th.text.strip() for th in header_items]
            csvwriter.writerow(header_texts + ["NAC"])

            last_row = None
            for tr in rows[1:]:
                cells = tr.find_all("td")
                is_new_row = bool(cells[0].text.strip())
                if is_new_row:
                    # Save previous row(s)
                    if last_row:
                        csvwriter.writerow(last_row)
                    
                    # Start new line; add columns from radio reference, then append NAC
                    last_row = []
                    for column_name in column_indices.keys():
                        # Skip "Freqs" and "NAC" since they are handled separately
                        if column_name in ["Freqs", "NAC"]:
                            continue

                        idx = column_indices[column_name]
                        val = cells[idx].text.strip() if len(cells)> idx else ""
                        last_row.append(val)
                    freqs_str = self._get_freqs_str(cells[column_indices.get("Freqs")])
                    last_row.append(freqs_str)
                    nac = self._get_nac_from_site_link(cells[column_indices.get("Name")])
                    last_row.append(nac)
                else:
                    # Same site, just adding more frequencies
                    freq_start_idx = column_indices.get("Freqs")
                    freqs_str = self._get_freqs_str(cells[freq_start_idx:])
                    last_row[freq_start_idx] += f",{freqs_str}"
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
