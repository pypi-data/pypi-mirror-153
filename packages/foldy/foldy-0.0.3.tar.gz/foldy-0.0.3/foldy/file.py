import os
import shutil


class File():

    def __init__(self, path: str):
        self.path = path

    def read(self, encoding: str = "utf-8", lines: bool = False):
        """Reads file"""
        with open(self.path, "r", encoding=encoding) as f:
            return f.readlines() if lines else f.read()

    def create(self):
        """Creates file if it doesn't exist"""
        if self.exists(): return

        with open(self.path, "x"):
            return

    def clean(self):
        """Cleans file, if it exists - creates empty file"""

        with open(self.path, "w") as f:
            f.write("")

    def move(self, new_path: str):
        shutil.move(self.path, new_path)

    def write(self, content: str | list):
        with open(self.path, "w") as f:

            if isinstance(content, str):
                return f.write(content)

            elif isinstance(content, list):
                return f.writelines(content)

    def delete(self):
        os.remove(self.path)

    def append(self, content: str | list):
        with open(self.path, "a") as f:

            if isinstance(content, str):
                return f.write(content)

            elif isinstance(content, list):
                return f.writelines(content)

    def exists(self) -> bool:
        return os.path.isfile(self.path)