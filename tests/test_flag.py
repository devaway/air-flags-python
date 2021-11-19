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
    "value,description,expiration_date",
    [
        (True, "New description", None),
        (True, "Other description", "2121-01-01"),
    ],
)
def test_flag_true(
    value: bool, description: str, expiration_date: str
) -> None:
    flag = Flag(
        value=value,
        description=description,
        expiration_date=expiration_date,
    )

    assert str(flag) == description
    assert bool(flag)


@pytest.mark.parametrize(
    "value,description,expiration_date",
    [
        (False, "New description", None),
        (False, "Other description", "2121-01-01"),
        (True, "Other description", "2000-01-01"),
    ],
)
def test_flag_false(
    value: bool, description: str, expiration_date: str
) -> None:
    flag = Flag(
        value=value,
        description=description,
        expiration_date=expiration_date,
    )

    assert str(flag) == description
    assert not bool(flag)


def test_flag_only_required_fields() -> None:
    flag = Flag(value=True)

    assert str(flag) == ""
    assert bool(flag)
