import random
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

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
MAX_PERCENTAGE = 100


@dataclass
class Rollout:
    """Rollout entity"""

    strategy: bool
    percentage: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    def __post_init__(self):
        if self.strategy not in ROLLOUT_STRATEGIES:
            raise ValueError(f"Field 'strategy' must be {ROLLOUT_STRATEGIES}")
        if self.percentage and self.percentage not in range(1, 100):
            raise ValueError("Field 'percentage' must be between 1 and 100")
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
        if not self.__is_on_date():
            return False
        if self.strategy == CANARY_STRATEGY:
            return self.__gen_canary_value()
        elif self.strategy == SCHEDULED_STRATEGY:
            return self.__gen_scheduled_value()
        elif self.strategy == PROGRESSIVE_STRATEGY:
            return self.__gen_progressive_value()
        return False

    def __gen_canary_value(self) -> bool:
        if not self.percentage:
            raise ValueError(
                "Field 'percentage' is required for Canary rollout"
            )

        return self.__random_value(self.percentage)

    def __gen_scheduled_value(self) -> bool:
        if self.percentage:
            return self.__random_value(self.percentage)
        return True

    def __gen_progressive_value(self) -> bool:
        if not self.percentage:
            raise ValueError(
                "Field 'percentage' is required for Progressive rollout"
            )

        # period = datetime.strptime(
        #     self.start_date, DATE_FORMAT
        # ) - datetime.strptime(self.end_date, DATE_FORMAT)
        # mult = (MAX_PERCENTAGE - self.percentage) / period.days
        # datetime.today() - datetime.strptime(self.end_date, DATE_FORMAT)

        return self.__random_value(self.percentage)

    def __random_value(self, percentage) -> bool:
        return random.choices(
            ROLLOUT_VALUES, [percentage, MAX_PERCENTAGE - percentage]
        )[0]

    def __is_on_date(self) -> bool:
        if self.start_date and self.end_date:
            return (
                datetime.strptime(str(self.start_date), DATE_FORMAT)
                <= datetime.today()
                <= datetime.strptime(str(self.end_date), DATE_FORMAT)
            )
        return True
