from dataclasses import dataclass
from typing import Optional

from air_flags.rollout import Rollout


@dataclass
class Flag:
    """Flag entity"""

    value: bool
    description: str = ""
    rollout: Optional[Rollout] = None

    def __str__(self) -> str:
        return self.description

    def __bool__(self) -> bool:
        if self.rollout:
            return self.rollout.value
        return self.value
