from typing import Any

import pytest

from air_flags.flag import Flag


@pytest.mark.parametrize(
    "value,description,expiration_date,message",
    [
        (123, "description", None, "Field 'value' must be of type 'bool'"),
        ("True", "description", None, "Field 'value' must be of type 'bool'"),
        ({}, "description", None, "Field 'value' must be of type 'bool'"),
        ([], "description", None, "Field 'value' must be of type 'bool'"),
        (True, 123, None, "Field 'description' must be of type 'str'"),
        (True, True, None, "Field 'description' must be of type 'str'"),
        (False, {}, None, "Field 'description' must be of type 'str'"),
        (False, [], None, "Field 'description' must be of type 'str'"),
        (
            False,
            "",
            123,
            "Field 'expiration_date' must be a date with the"
            " format 'YYYY-mm-dd'",
        ),
        (
            True,
            "",
            "11-11-2011",
            "Field 'expiration_date' must be a date with the"
            " format 'YYYY-mm-dd'",
        ),
        (
            True,
            "",
            False,
            "Field 'expiration_date' must be a date with the"
            " format 'YYYY-mm-dd'",
        ),
    ],
)
def test_flag_invalid_type_param(
    value: Any, description: Any, expiration_date: Any, message: str
) -> None:
    with pytest.raises(TypeError) as e:
        Flag(
            value=value,
            description=description,
            expiration_date=expiration_date,
        )

    assert str(e.value.args[0]) == message


@pytest.mark.freeze_time("2021-11-19")
@pytest.mark.parametrize(
    "expiration_date,expected",
    [
        ("2022-01-01", False),
        ("2000-01-01", True),
    ],
)
def test_flag_is_expired(expiration_date: str, expected: bool) -> None:
    flag = Flag(
        value=False,
        expiration_date=expiration_date,
    )

    assert flag.is_expired == expected


@pytest.mark.freeze_time("2021-11-19")
@pytest.mark.parametrize(
    "value,description,expiration_date",
    [
        (True, "New description", None),
        (True, "Other description", "2022-01-01"),
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


@pytest.mark.freeze_time("2021-11-19")
@pytest.mark.parametrize(
    "value,description,expiration_date",
    [
        (False, "New description", None),
        (False, "Other description", "2022-01-01"),
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
