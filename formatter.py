import os


class Formatter:
    def __init__(self, indir: str, outdir: str):
        self.indir = indir
        self.outdir = outdir

    def format(self):
        os.makedirs(self.outdir, exist_ok=True)
