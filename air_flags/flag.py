from dataclasses import dataclass
from typing import List, Optional, Union

from air_flags.rollout import Rollout


@dataclass
class Flag:
    """Flag entity"""

    value: bool
    description: str = ""
    selectived: Optional[Union[str, List]] = None
    rollout: Optional[Rollout] = None

    def __str__(self) -> str:
        return self.description

    def __bool__(self) -> bool:
        if self.rollout:
            return self.rollout.value
        return self.value

    def __call__(self, selected: str) -> bool:
        if self.selectived:
            if (
                isinstance(self.selectived, str)
                and selected == self.selectived
            ):
                return True

            if (
                isinstance(self.selectived, list)
                and selected in self.selectived
            ):
                return True

        return bool(self)
