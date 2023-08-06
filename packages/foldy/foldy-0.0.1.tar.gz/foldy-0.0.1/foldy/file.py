import os


class File():

    def __init__(self, path: str):
        self.path = path

    def read(self, encoding: str = "utf-8", lines: bool = False):
        try:

            with open(self.path, "r", encoding=encoding) as f:

                return f.readlines() if lines else f.read()

        except Exception as e:
            print(e)

    def create(self):
        with open(self.path, "x"):
            return

    def write(self, content: str | list):
        try:

            with open(self.path, "w") as f:

                if isinstance(content, str):
                    return f.write(content)

                elif isinstance(content, list):
                    return f.writelines(content)

        except Exception as e:
            print(e)

    def append(self, content: str | list):
        try:

            with open(self.path, "a") as f:

                if isinstance(content, str):
                    return f.write(content)

                elif isinstance(content, list):
                    return f.writelines(content)

        except Exception as e:
            print(e)

    def exists(self) -> bool:
        return os.path.isfile(self.path)