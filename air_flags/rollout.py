from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from air_flags.utils import calc_progressive_percentage, generate_random_value

ROLLOUT_VALUES = [True, False]
DATE_FORMAT = "%Y-%m-%d"
CANARY_STRATEGY = "canary"
SCHEDULED_STRATEGY = "scheduled"
PROGRESSIVE_STRATEGY = "progressive"
ROLLOUT_STRATEGIES = [
    CANARY_STRATEGY,
    SCHEDULED_STRATEGY,
    PROGRESSIVE_STRATEGY,
]
MIN_PERCENTAGE = 0
MAX_PERCENTAGE = 100


@dataclass
class Rollout:
    """Rollout entity"""

    strategy: str
    percentage: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    def __post_init__(self):
        if self.strategy not in ROLLOUT_STRATEGIES:
            raise ValueError(f"Field 'strategy' must be {ROLLOUT_STRATEGIES}")
        if self.percentage is not None and self.percentage not in range(
            MIN_PERCENTAGE, MAX_PERCENTAGE + 1
        ):
            raise ValueError("Field 'percentage' must be between 0 and 100")
        if self.start_date:
            try:
                datetime.strptime(str(self.start_date), DATE_FORMAT)
            except ValueError:
                raise ValueError(
                    "Field 'start_date' must be a date with the"
                    " format 'YYYY-mm-dd'"
                )
        if self.end_date:
            try:
                datetime.strptime(str(self.end_date), DATE_FORMAT)
            except ValueError:
                raise ValueError(
                    "Field 'end_date' must be a date with the"
                    " format 'YYYY-mm-dd'"
                )

    @property
    def value(self) -> bool:
        if not self._is_on_date():
            return False
        if self.strategy == CANARY_STRATEGY:
            return self._gen_canary_value()
        if self.strategy == SCHEDULED_STRATEGY:
            return self._gen_scheduled_value()
        if self.strategy == PROGRESSIVE_STRATEGY:
            return self._gen_progressive_value()
        return False

    def _gen_canary_value(self) -> bool:
        if not self.percentage:
            raise ValueError(
                "Field 'percentage' is required for Canary rollout"
            )

        return generate_random_value(
            ROLLOUT_VALUES, self.percentage, MAX_PERCENTAGE
        )

    def _gen_scheduled_value(self) -> bool:
        if not self.start_date or not self.end_date:
            raise ValueError(
                "Fields 'start_date' and 'end_date' are required for"
                " Scheduled rollout"
            )
        if not self.percentage:
            return True

        return generate_random_value(
            ROLLOUT_VALUES, self.percentage, MAX_PERCENTAGE
        )

    def _gen_progressive_value(self) -> bool:
        if not self.start_date or not self.end_date:
            raise ValueError(
                "Fields 'start_date' and 'end_date' are required for"
                " Progressive rollout"
            )
        if not self.percentage:
            raise ValueError(
                "Field 'percentage' is required for Progressive rollout"
            )

        progressive_percentage = calc_progressive_percentage(
            self.percentage,
            self.start_date,
            self.end_date,
            MAX_PERCENTAGE,
            DATE_FORMAT,
        )

        return generate_random_value(
            ROLLOUT_VALUES, progressive_percentage, MAX_PERCENTAGE
        )

    def _is_on_date(self) -> bool:
        if self.start_date and self.end_date:
            return (
                datetime.strptime(str(self.start_date), DATE_FORMAT)
                <= datetime.today()
                <= datetime.strptime(str(self.end_date), DATE_FORMAT)
            )
        return True
