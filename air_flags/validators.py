import os
import pathlib
from typing import List

TYPE_JSON = ".json"
TYPE_YAML = ".yaml"
VALID_CONFIG_TYPES = [
    TYPE_JSON,
    TYPE_YAML,
]
SCHEMA_VALIDATOR = {
    "type": "object",
    "properties": {
        "value": {"type": "boolean"},
        "description": {"type": "string"},
        "rollout": {
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
                "percentage": {"type": "number"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"},
            },
        },
    },
    "required": ["value"],
}


class TypeValidator:
    def __init__(self, types: List[str]):
        self.types = types

    def run(self, filepath: str) -> str:
        ext = pathlib.Path(filepath).suffix
        if ext not in self.types:
            raise ValueError("The provided config type is not supported")
        return ext


class PathValidator:
    def run(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            raise ValueError("We can't find the provided config file")
        return filepath
