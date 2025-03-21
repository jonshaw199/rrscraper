import bs4
import csv
import os

from scraper import Scraper


class ConventionalScraper(Scraper):
    def __init__(self, url: str, out_dir: str = None):
        super().__init__(url, out_dir)

    def scrape(self):
        super().scrape()
        os.mkdir(f"{self.out_dir}/freqs")
        self.__export_freqs()

    def __export_freqs(self):
        container = self._soup.find(id="freqs")
        groups = container.find_all("div", recursive=False)

        header_row = [
            "Frequency",
            "License",
            "Type",
            "Tone",
            "Alpha Tag",
            "Description",
            "Mode",
            "Tag",
        ]

        for group in groups:
            group_header = group.find("h4")
            group_name = self._get_text_from_tag(group_header)
            dir_name = self._to_filename(group_name)
            os.mkdir(f"{self.out_dir}/freqs/{dir_name}")
            headers = group.find_all("h5")
            for header in headers:
                table = header.find_next("table")
                if self.__is_scrapable(table):
                    header_text = self._get_text_from_tag(header)
                    filename = self._to_filename(header_text)
                    rows = table.find("tbody").find_all("tr")
                    with open(
                        f"{self.out_dir}/freqs/{dir_name}/{filename}.csv", "w"
                    ) as file:
                        writer = csv.writer(file)
                        writer.writerow(header_row)
                        for row in rows:
                            cells = row.find_all("td")
                            cell_texts = map(
                                lambda cell: self._get_text_from_tag(cell), cells
                            )
                            writer.writerow(cell_texts)

    # We currently expect the frequency table to be in a predictable format with the same 8 columns
    def __is_scrapable(self, tag: bs4.Tag):
        if not tag:
            return False
        header_row = tag.find("thead")
        if not header_row:
            return False
        header_cells = header_row.find_all("th")
        if len(header_cells) != 8:
            return False
        first_header_cell = header_cells[0]
        if not first_header_cell:
            return False
        first_header_cell_text = self._get_text_from_tag(first_header_cell)
        if first_header_cell_text != "Frequency":
            return False
        body_rows = tag.find_all("tr")
        if not (body_rows and len(body_rows)):
            return False
        return True
