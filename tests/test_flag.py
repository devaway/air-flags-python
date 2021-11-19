from typing import Any

import pytest

from air_flags.flag import Flag


@pytest.mark.parametrize(
    "value,description,message",
    [
        (123, "description", "Field 'value' must be of type 'bool'"),
        ("True", "description", "Field 'value' must be of type 'bool'"),
        ({}, "description", "Field 'value' must be of type 'bool'"),
        ([], "description", "Field 'value' must be of type 'bool'"),
        (True, 123, "Field 'description' must be of type 'str'"),
        (True, True, "Field 'description' must be of type 'str'"),
        (False, {}, "Field 'description' must be of type 'str'"),
        (False, [], "Field 'description' must be of type 'str'"),
    ],
)
def test_flag_invalid_type_param(
    value: Any, description: Any, message: str
) -> None:
    with pytest.raises(TypeError) as e:
        Flag(
            value=value,
            description=description,
        )

    assert str(e.value.args[0]) == message


@pytest.mark.parametrize(
    "value,description",
    [
        (True, "New description"),
        (False, "Other description"),
    ],
)
def test_flag_ok(value: bool, description: str) -> None:
    flag = Flag(
        value=value,
        description=description,
    )

    assert str(flag) == description
    assert bool(flag) == value
