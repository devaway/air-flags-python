from typing import Any

import pytest

from air_flags.flag import Flag


def test_flag_only_required_fields() -> None:
    flag = Flag(value=True)

    assert str(flag) == ""
    assert bool(flag)


def test_flag_with_description() -> None:
    flag = Flag(value=True, description="This is an amazing flag")

    assert str(flag) == "This is an amazing flag"
    assert bool(flag)


@pytest.mark.parametrize(
    "val,sel,selected,expected",
    [
        (False, ["1234", "5678"], "1234", True),
        (True, ["1234", "5678"], "1234", True),
        (False, ["1234", "5678"], "abcd", False),
        (True, ["1234", "5678"], "abcd", True),
        (False, "1234", "abcde", False),
        (True, "1234", "abcde", True),
        (False, "1234", "1234", True),
        (True, "1234", "1234", True),
        (True, None, "1234", True),
    ],
)
def test_flag_with_selective(
    val: bool, sel: Any, selected: str, expected: bool
) -> None:
    flag = Flag(
        value=val,
        description="This is an amazing flag",
        selective=sel,
    )

    assert str(flag) == "This is an amazing flag"
    assert bool(flag(selected)) == expected
