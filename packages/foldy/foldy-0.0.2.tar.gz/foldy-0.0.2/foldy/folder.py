import contextlib
import os
import sys
import shutil


class Folder():

    def __init__(self, path: str):
        self.path = path

    def create(self):
        with contextlib.suppress(FileExistsError):
            os.mkdir(self.path)

    def move(self, new_path: str):
        shutil.move(self.path, new_path)

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    def delete(self):
        shutil.rmtree('/folder_name', ignore_errors=True)