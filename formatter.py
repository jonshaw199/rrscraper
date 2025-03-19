import os


class Formatter:
    def __init__(self, in_dir: str, out_dir: str):
        self.in_dir = in_dir
        self.out_dir = out_dir

    def format(self):
        os.makedirs(self.out_dir, exist_ok=True)
