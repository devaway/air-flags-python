from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Flag:
    """Flag entity"""

    value: bool
    description: str = ""
    expiration_date: Optional[str] = None

    def __post_init__(self):
        if type(self.value) is not bool:
            raise TypeError("Field 'value' must be of type 'bool'")
        if type(self.description) is not str:
            raise TypeError("Field 'description' must be of type 'str'")
        if self.expiration_date:
            try:
                datetime.strptime(self.expiration_date, "%Y-%m-%d")
            except ValueError:
                raise TypeError(
                    "Field 'expiration_date' must be a date with the"
                    " format 'YYYY-mm-dd'"
                )

    def __str__(self) -> str:
        return self.description

    def __bool__(self) -> bool:
        if self.expiration_date and (
            datetime.today()
            > datetime.strptime(self.expiration_date, "%Y-%m-%d")
        ):
            return False
        return self.value
