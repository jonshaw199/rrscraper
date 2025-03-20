import os


class Formatter:
    def __init__(self, in_dir: str, out_dir: str):
        self._in_dir = in_dir
        self._out_dir = out_dir

    def format(self):
        os.makedirs(self._out_dir, exist_ok=True)
