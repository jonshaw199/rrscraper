import csv
import os

from formatter import Formatter


class Op25Formatter(Formatter):
    def __init__(self, indir: str):
        super().__init__(indir, f"{indir}/op25")
        self._load_sites_and_freqs()

    def format(self):
        super().format()
        self._generate_trunk_file()
        self._generate_tgids_file()

    def _load_sites_and_freqs(self):
        sites_and_freqs = []
        with open(f"{self.indir}/sites_and_freqs.csv", newline="") as file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                # Get only control channels (ending in "c")
                freqs = [
                    freq[:-1] for freq in row["Freqs"].split(",") if freq.endswith("c")
                ]
                sites_and_freqs.append(
                    [row["Site"], row["Name"], row["County"], freqs, row["NAC"]]
                )
        self.sites_and_freqs = sites_and_freqs

    def _generate_tgids_file(self):
        with open(f"{self.outdir}/tgids.tsv", "w", newline="") as outfile:
            writer = csv.writer(outfile, delimiter="\t", quoting=csv.QUOTE_ALL)
            for filename in os.listdir(f"{self.indir}/talkgroups"):
                with open(f"{self.indir}/talkgroups/{filename}", newline="") as infile:
                    reader = csv.DictReader(infile)
                    for row in reader:
                        text = f"{row['Alpha Tag']}: {row['Description']}"
                        writer.writerow([row["DEC"], text])

    def _generate_trunk_file(self):
        siteIdx = self._prompt_for_site()
        site_id, site_name, county, control_freqs, nac = self.sites_and_freqs[siteIdx]
        nac_int = int(nac, 16)
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
            str(nac_int),
            "cqpsk",
            "tgids.tsv",
            "",
            "",
            "",
        ]
        with open(f"{self.outdir}/trunk.tsv", "w", newline="") as tsvfile:
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
