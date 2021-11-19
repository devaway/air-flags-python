import json
from typing import Any, List, Mapping

import yaml

from air_flags.flag import Flag
from air_flags.path_validator import PathValidator
from air_flags.type_validator import TypeValidator

TYPE_JSON = ".json"
TYPE_YAML = ".yaml"
VALID_CONFIG_TYPES = [
    TYPE_JSON,
    TYPE_YAML,
]


class AirFlag:
    """AirFlag configuration
    Load configuration from json and yaml files
    and set the flags entity as class attrs
    """

    def __init__(
        self,
        filepath: str = "",
    ) -> None:
        self.type = TypeValidator(VALID_CONFIG_TYPES).run(filepath)
        self.path = PathValidator().run(filepath)
        self.config = self.__get_config()

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
