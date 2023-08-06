import contextlib
import os
import sys


class Folder():

    def __init__(self, path: str):
        self.path = path

    def create(self):
        with contextlib.suppress(FileExistsError):
            os.mkdir(self.path)

    def exists(self) -> bool:
        return os.path.isdir(self.path)