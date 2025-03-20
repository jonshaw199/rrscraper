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
        self.__export_details()
        self.__export_sites_and_freqs()
        os.mkdir(f"{self.out_dir}/talkgroups")
        self.__export_talkgroups()

    def __export_details(self):
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
                    self.__get_detail_by_label("System Name:"),
                    self.__get_detail_by_label("Location:"),
                    self.__get_detail_by_label("County:"),
                    self.__get_detail_by_label("System Type:"),
                    self.__get_detail_by_label("System Voice:"),
                    self.__get_detail_by_label("System ID:"),
                ]
            )

    def __get_detail_by_label(self, label: str, soup: BeautifulSoup = None) -> str:
        th_tag = (soup or self._soup).find("th", string=label)
        if th_tag:
            td_tag = th_tag.find_next("td")
            return self._get_text_from_tag(td_tag)
        return ""

    def __export_sites_and_freqs(self):
        header = self._soup.find("h3", string="Sites and Frequencies")
        table = header.find_next("table")
        rows = table.find_all("tr")
        header_items = rows[0].find_all('th')

        # Map column names to their indices
        column_indices = {}
        for idx, th in enumerate(header_items):
            column_name = self._get_text_from_tag(th)
            if column_name:
                column_indices[column_name] = idx

        # Open CSV file for writing
        with open(f"{self.out_dir}/sites_and_freqs.csv", "w") as file:
            csvwriter = csv.writer(file)

            # Write the header row, including "NAC"
            header_texts = [self._get_text_from_tag(th) for th in header_items]
            csvwriter.writerow(header_texts + ["NAC"])

            last_row = None
            for tr in rows[1:]:
                cells = tr.find_all("td")
                is_new_row = bool(self._get_text_from_tag(cells[0]))
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
                        val = self._get_text_from_tag(cells[idx]) if len(cells)> idx else ""
                        last_row.append(val)
                    freqs_start_idx = column_indices.get("Freqs")
                    freqs_str = self.__get_freqs_str(cells[freqs_start_idx:])
                    last_row.append(freqs_str)
                    site_idx = column_indices.get("Name")
                    nac = self.__get_nac_from_site_link(cells[site_idx])
                    last_row.append(nac)
                else:
                    # Same site, just adding more frequencies
                    freq_start_idx = column_indices.get("Freqs")
                    freqs_str = self.__get_freqs_str(cells[freq_start_idx:])
                    last_row[freq_start_idx] += f",{freqs_str}"
            csvwriter.writerow(last_row)

    def __get_nac_from_site_link(self, cell: Tag):
        link_tag = cell.find("a")
        url = f"{base_url}{link_tag['href']}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        nac = self.__get_detail_by_label("NAC:", soup)
        if not nac or nac == "N/A":
            return ""
        return f"0x{nac}"

    def __get_freqs_str(self, tags: List[Tag]):
        texts = map(lambda tag: self._get_text_from_tag(tag), tags)
        filtered_texts = filter(lambda text: bool(text), texts)
        return ",".join(filtered_texts)

    def __export_talkgroups(self):
        header = self._soup.find("h3", string="Talkgroups")
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


def to_filename(text: str) -> str:
    return "".join(x for x in text if x.isalnum())
