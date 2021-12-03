import pytest

from air_flags.utils import calc_progressive_percentage

DATE_FORMAT = "%Y-%m-%d"
MAX_VALUE = 100


@pytest.mark.freeze_time("2021-10-30")
def test_calc_progressive_percentage_0_percentage(freezer) -> None:

    assert (
        calc_progressive_percentage(
            0, "2021-11-01", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 0
    )

    freezer.move_to("2021-11-01")
    assert (
        calc_progressive_percentage(
            10, "2021-11-01", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 10
    )

    freezer.move_to("2021-11-03")
    assert (
        calc_progressive_percentage(
            10, "2021-11-01", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 30
    )

    freezer.move_to("2021-11-06")
    assert (
        calc_progressive_percentage(
            10, "2021-11-01", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 60
    )

    freezer.move_to("2021-11-10")
    assert (
        calc_progressive_percentage(
            10, "2021-11-01", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 100
    )


@pytest.mark.freeze_time("2021-09-01")
def test_calc_progressive_percentage_with_percentage(freezer) -> None:

    assert (
        calc_progressive_percentage(
            50, "2021-09-02", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 0
    )

    freezer.move_to("2021-09-29")
    assert (
        calc_progressive_percentage(
            50, "2021-09-02", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 69
    )

    freezer.move_to("2021-10-07")
    assert (
        calc_progressive_percentage(
            50, "2021-09-02", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 75
    )

    freezer.move_to("2021-11-10")
    assert (
        calc_progressive_percentage(
            50, "2021-09-02", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 100
    )

    freezer.move_to("2021-11-11")
    assert (
        calc_progressive_percentage(
            50, "2021-09-02", "2021-11-10", MAX_VALUE, DATE_FORMAT
        )
        == 0
    )
