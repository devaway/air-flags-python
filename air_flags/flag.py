from dataclasses import dataclass
from typing import List, Optional, Union

from air_flags.rollout import Rollout


@dataclass
class Flag:
    """Flag entity"""

    value: bool
    description: str = ""
    selective: Optional[Union[str, List]] = None
    rollout: Optional[Rollout] = None

    def __str__(self) -> str:
        return self.description

    def __bool__(self) -> bool:
        if self.rollout:
            return self.rollout.value
        return self.value

    def __call__(self, selected) -> bool:
        if not self:
            return False

        if not self.selective or selected != self.selective:
            return False

        return True
