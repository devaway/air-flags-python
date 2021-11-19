import pathlib
from typing import List


class TypeValidator:
    def __init__(self, types: List[str]):
        self.types = types

    def run(self, filepath: str) -> str:
        ext = pathlib.Path(filepath).suffix
        if ext not in self.types:
            raise ValueError("The provided config type is not supported")
        return ext
