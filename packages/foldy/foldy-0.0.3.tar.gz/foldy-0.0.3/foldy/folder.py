import shutil
import os


class Folder():

    def __init__(self, path: str):
        self.path = path

    def create(self):
        if self.exists(): return
        os.mkdir(self.path)

    def move(self, new_path: str):
        shutil.move(self.path, new_path)

    def exists(self) -> bool:
        return os.path.isdir(self.path)

    def delete(self):
        shutil.rmtree(self.path, ignore_errors=True)