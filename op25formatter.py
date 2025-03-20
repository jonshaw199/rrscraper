import csv
import os

from formatter import Formatter


class Op25Formatter(Formatter):
    def __init__(self, in_dir: str):
        super().__init__(in_dir, f"{in_dir}/op25")
        self._load_sites_and_freqs()

    def format(self):
        super().format()
        self._generate_trunk_file()
        self._generate_tgids_file()

    def _load_sites_and_freqs(self):
        sites_and_freqs = []
        with open(f"{self.in_dir}/sites_and_freqs.csv", newline="") as file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                # Get only control channels (ending in "c")
                freqs = [
                    freq[:-1] for freq in row["Freqs"].split(",") if freq.endswith("c")
                ]
                sites_and_freqs.append(
                    [row["Site"], row["Name"], row.get("County", "Unknown County"), freqs, row["NAC"]]
                )
        self.sites_and_freqs = sites_and_freqs

    def _generate_tgids_file(self):
        with open(f"{self.out_dir}/tgids.tsv", "w", newline="") as outfile:
            writer = csv.writer(outfile, delimiter="\t", quoting=csv.QUOTE_ALL)
            for filename in os.listdir(f"{self.in_dir}/talkgroups"):
                with open(f"{self.in_dir}/talkgroups/{filename}", newline="") as infile:
                    reader = csv.DictReader(infile)
                    for row in reader:
                        text = f"{row['Alpha Tag']}: {row['Description']}"
                        writer.writerow([row["DEC"], text])

    def _generate_trunk_file(self):
        site_idx = self._prompt_for_site()
        site_id, site_name, county, control_freqs, nac = self.sites_and_freqs[site_idx]
        control_channels = ",".join(control_freqs)
        header = [
            "Sysname",
            "Control Channel List",
            "Offset",
            "NAC",
            "Modulation",
            "TGID Tags File",
            "Whitelist",
            "Blacklist",
            "Center Frequency",
        ]
        data = [
            f"{site_name} ({county}; {site_id})",
            control_channels,
            "0",
            f"0x{nac}" if nac else "0",
            "cqpsk",
            "tgids.tsv",
            "",
            "",
            "",
        ]
        with open(f"{self.out_dir}/trunk.tsv", "w", newline="") as tsvfile:
            writer = csv.writer(tsvfile, delimiter="\t", quoting=csv.QUOTE_ALL)
            writer.writerow(header)
            writer.writerow(data)

    def _prompt_for_site(self):
        print(f"\n\n{'*' * 30}\nSelect a site:")
        for idx, site in enumerate(self.sites_and_freqs, start=1):
            print(f"{idx}. {site[1]} ({site[2]}; {site[0]})")
        print(f"{'*' * 30}\n\n")

        num_sites = len(self.sites_and_freqs)
        while True:
            msg = f"Enter a number from 1-{num_sites}: "
            try:
                selected_idx = int(input(msg))
                if 1 <= selected_idx <= num_sites:
                    return selected_idx - 1
                else:
                    raise ValueError("Invalid input")
            except ValueError as e:
                print(e)
