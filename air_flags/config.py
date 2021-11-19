import json
import os
import pathlib
from functools import wraps
from typing import Any, Callable, List, Mapping

import yaml

from air_flags.flag import Flag

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
        self.type = self.__valid_type(filepath)
        self.path = self.__valid_path(filepath)
        self.config = self.__get_config()

    def __valid_type(self, filepath: str) -> str:
        ext = pathlib.Path(filepath).suffix
        if ext not in VALID_CONFIG_TYPES:
            raise ValueError("The provided config type is not supported")
        return ext

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

    def __getattr__(self, attr) -> None:
        if attr not in self.config:
            raise Exception("We can't find the requested flag")

    def is_active(self, flag: str) -> Callable:
        """Air flag decorator to validate if a flag is actived"""

        def _is_active_flag(func: Callable) -> Callable:
            @wraps(func)
            def wrapped(*args: List, **kwargs: Mapping) -> Callable:
                if not getattr(self, flag):
                    raise Exception("We can't find the requested flag")
                return func(*args, **kwargs)

            return wrapped

        return _is_active_flag
