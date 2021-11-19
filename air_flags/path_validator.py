import os


class PathValidator:
    def run(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            raise ValueError("We can't find the provided config file")
        return filepath
