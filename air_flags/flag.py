from dataclasses import dataclass


@dataclass
class Flag:
    """Flag entity"""
    value: bool
    description: str

    def __post_init__(self):
        if type(self.value) is not bool:
            raise TypeError("Field 'value' must be of type 'bool'")
        if type(self.description) is not str:
            raise TypeError("Field 'description' must be of type 'str'")

    def __str__(self) -> str:
        return self.description

    def __bool__(self) -> bool:
        return self.value
