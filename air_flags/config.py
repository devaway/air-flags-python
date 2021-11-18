import json
import os
from typing import Any, Mapping

import yaml

from air_flags.flag import Flag

TYPE_JSON = "json"
TYPE_YAML = "yaml"
VALID_CONFIG_TYPES = [
    TYPE_JSON,
    TYPE_YAML,
]


class AirFlag:
    def __init__(
        self,
        filetype: str = "",
        filepath: str = "",
    ) -> None:
        self.type = self.__valid_type(filetype)
        self.path = self.__valid_path(filepath)
        self.config = self.__get_config()

    def __valid_type(self, filetype: str) -> str:
        if filetype not in VALID_CONFIG_TYPES:
            raise ValueError("The provided config type is not supported")
        return filetype

    def __valid_path(self, filepath: str) -> str:
        if not os.path.isfile(filepath):
            raise ValueError("We can't find the provided config file")
        return filepath

    def __get_config(self) -> Mapping[Any, Any]:
        config: Mapping[Any, Any] = {}
        with open(self.path, "r") as f:
            if self.type == TYPE_JSON:
                config = json.load(f)

            if self.type == TYPE_YAML:
                config = yaml.load(f, Loader=yaml.SafeLoader)

        if not config:
            raise Exception("We can't find any air flag")

        for flag in config.keys():
            self.__setattr__(flag, Flag(**config.get(flag, {})))

        return config

    def __getattr__(self, attr):
        if attr not in self.config:
            raise Exception("We can't find the requested flag")
