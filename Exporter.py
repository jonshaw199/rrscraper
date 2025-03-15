from os import mkdir
from time import time


class Exporter:
    def __init__(self, outdir: str = None):
        self.outdir = outdir or str(time())

    def export(self):
        mkdir(self.outdir)
