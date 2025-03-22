import csv
import os
import re
from typing import List

from .formatter import Formatter

chirp_headers = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone", "rToneFreq", "cToneFreq",
    "DtcsCode", "DtcsPolarity", "RxDtcsCode", "CrossMode", "Mode", "TStep", "Skip", "Power",
    "Comment", "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE"
]



class ChirpFormatter(Formatter):
    def __init__(self, in_dir: str):
        super().__init__(in_dir, f"{in_dir}/chirp")
    
    def format(self):
        super().format()
        with open(f"{self._out_dir}/freqs.csv", "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(chirp_headers)
            location = 0
            for filename in self.__get_filenames():
                with open(filename, newline="") as infile:
                    reader = csv.DictReader(infile)
                    for row in reader:
                        mode = self.__transform_mode(row["Mode"])

                        # Skip unsupported modes
                        if mode not in ["FM", "NFM", "WFM"]:
                            continue

                        tone = self.__transform_tone(row["Tone"], mode)
                        comment = f"{row["Description"]} ({row["Tag"]})"
                        chirp_row = [
                            location,               # Location
                            row["Alpha Tag"],       # Name
                            row["Frequency"],       # Frequency
                            "",                     # Duplex
                            0.000000,               # Offset
                            "",                     # Tone
                            tone,                   # rToneFreq
                            tone,                   # cToneFreq
                            "023",                  # DtcsCode
                            "NN",                   # DtcsPolarity
                            "023",                  # RxDtcsCode
                            "Tone->Tone",           # CrossMode
                            mode,                   # Mode
                            "5.00",                 # TStep
                            "",                     # Skip
                            "4.0W",                 # Power
                            comment,                # Comment
                            "",                     # URCALL
                            "",                     # RPT1CALL
                            "",                     # RPT2CALL
                            ""                      # DVCODE
                        ]
                        writer.writerow(chirp_row)
                        location += 1

    def __get_filenames(self) -> List[str]:
        result = []
        for root, dirs, files in os.walk(f"{self._in_dir}/freqs"):
            for filename in files:
                if filename.endswith('.csv'):
                    result.append(os.path.join(root, filename))
        return result

    def __transform_mode(self, mode: str) -> str:
        match mode:
            case "FMN":
                return "NFM"
            case "FMW":
                return "WFM"
            case _:
                return mode

    def __transform_tone(self, tone: str, mode: str) -> float:
        if mode in ["NFM", "FM"]:
            match = re.search(r'\d+(\.\d+)', tone)
            if match:
                return float(match.group(0))
        return 88.5
