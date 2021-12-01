from air_flags.flag import Flag


def test_flag_only_required_fields() -> None:
    flag = Flag(value=True)

    assert str(flag) == ""
    assert bool(flag)


def test_flag_with_description() -> None:
    flag = Flag(value=True, description="This is an amazing flag")

    assert str(flag) == "This is an amazing flag"
    assert bool(flag)
