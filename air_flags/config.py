import json
from functools import wraps
from typing import Any, Callable, List, Mapping, Optional

import jsonschema  # type: ignore
import yaml

from air_flags.flag import Flag
from air_flags.rollout import Rollout
from air_flags.validators import (
    SCHEMA_VALIDATOR,
    TYPE_JSON,
    TYPE_YAML,
    VALID_CONFIG_TYPES,
    PathValidator,
    TypeValidator,
)


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
            jsonschema.validate(
                instance=config.get(flag), schema=SCHEMA_VALIDATOR
            )
            if config.get(flag, {}).get("rollout"):
                config[flag]["rollout"] = Rollout(**config[flag]["rollout"])
            self.__setattr__(flag, Flag(**config.get(flag, {})))

        return config

    def __getattr__(self, attr) -> None:
        if attr not in self.config:
            raise Exception("We can't find the requested flag")

    def is_active(self, flag: str) -> Callable:
        """Air flag decorator to validate if a flag is actived"""

        def _is_active_flag(func: Callable) -> Callable:
            @wraps(func)
            def wrapped(*args: List, **kwargs: Mapping) -> Optional[Callable]:
                if not getattr(self, flag):
                    return None
                return func(*args, **kwargs)

            return wrapped

        return _is_active_flag
