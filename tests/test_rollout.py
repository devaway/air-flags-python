from typing import Any

import pytest

from air_flags.rollout import Rollout
from tests.mocks.rollout import MOCK_CANARY, MOCK_PROGRESSIVE, MOCK_SCHEDULED


@pytest.mark.parametrize(
    "strategy,percentage,start_date,end_date,message",
    [
        (
            "invalid",
            None,
            None,
            None,
            "Field 'strategy' must be ['canary', 'scheduled', 'progressive']",
        ),
        (
            MOCK_CANARY,
            -1,
            None,
            None,
            "Field 'percentage' must be between 0 and 100",
        ),
        (
            MOCK_CANARY,
            105,
            None,
            None,
            "Field 'percentage' must be between 0 and 100",
        ),
        (
            MOCK_SCHEDULED,
            None,
            "2020/11/21",
            None,
            "Field 'start_date' must be a date with the format 'YYYY-mm-dd'",
        ),
        (
            MOCK_SCHEDULED,
            None,
            None,
            "21-01-2000",
            "Field 'end_date' must be a date with the format 'YYYY-mm-dd'",
        ),
    ],
)
def test_rollout_value_error(
    strategy: Any,
    percentage: Any,
    start_date: Any,
    end_date: Any,
    message: str,
) -> None:
    with pytest.raises(ValueError) as e:
        Rollout(
            strategy=strategy,
            percentage=percentage,
            start_date=start_date,
            end_date=end_date,
        )

    assert str(e.value.args[0]) == message


def test_rollout_invalid_canary() -> None:
    with pytest.raises(ValueError) as e:
        rollout = Rollout(strategy=MOCK_CANARY)
        rollout.value

    assert (
        str(e.value.args[0])
        == "Field 'percentage' is required for Canary rollout"
    )


def test_rollout_valid_canary() -> None:
    rollout = Rollout(strategy=MOCK_CANARY, percentage=100)

    assert rollout.value


def test_rollout_invalid_scheduled() -> None:
    with pytest.raises(ValueError) as e:
        rollout = Rollout(strategy=MOCK_SCHEDULED)
        rollout.value

    assert (
        str(e.value.args[0])
        == "Fields 'start_date' and 'end_date' are required for"
        " Scheduled rollout"
    )


@pytest.mark.freeze_time("2021-11-19")
def test_rollout_scheduled_without_percentage() -> None:
    rollout = Rollout(
        strategy=MOCK_SCHEDULED,
        start_date="2021-11-01",
        end_date="2021-12-01",
    )

    assert rollout.value


@pytest.mark.freeze_time("2021-11-19")
def test_rollout_scheduled_with_percentage() -> None:
    rollout = Rollout(
        strategy=MOCK_SCHEDULED,
        percentage=100,
        start_date="2021-11-01",
        end_date="2021-12-01",
    )

    assert rollout.value


@pytest.mark.freeze_time("2021-11-19")
def test_rollout_progressive_without_date() -> None:
    with pytest.raises(ValueError) as e:
        rollout = Rollout(strategy=MOCK_PROGRESSIVE, percentage=50)
        rollout.value

    assert (
        str(e.value.args[0])
        == "Fields 'start_date' and 'end_date' are required for"
        " Progressive rollout"
    )


@pytest.mark.freeze_time("2021-11-19")
def test_rollout_progressive_without_percentage() -> None:
    with pytest.raises(ValueError) as e:
        rollout = Rollout(
            strategy=MOCK_PROGRESSIVE,
            start_date="2021-11-01",
            end_date="2021-12-01",
        )
        rollout.value

    assert (
        str(e.value.args[0])
        == "Field 'percentage' is required for Progressive rollout"
    )


@pytest.mark.freeze_time("2021-11-01")
def test_rollout_progressive_calc_percent(freezer) -> None:
    rollout = Rollout(
        strategy=MOCK_PROGRESSIVE,
        percentage=10,
        start_date="2021-11-01",
        end_date="2021-11-10",
    )

    assert (
        rollout._calc_progressive_percentage(10, "2021-11-01", "2021-11-10")
        == 10
    )

    freezer.move_to("2021-11-03")
    assert (
        rollout._calc_progressive_percentage(10, "2021-11-01", "2021-11-10")
        == 30
    )

    freezer.move_to("2021-11-06")
    assert (
        rollout._calc_progressive_percentage(10, "2021-11-01", "2021-11-10")
        == 60
    )

    freezer.move_to("2021-11-10")
    assert (
        rollout._calc_progressive_percentage(10, "2021-11-01", "2021-11-10")
        == 100
    )


@pytest.mark.freeze_time("2021-11-10")
def test_rollout_progressive_at_end_date() -> None:
    rollout = Rollout(
        strategy=MOCK_PROGRESSIVE,
        percentage=10,
        start_date="2021-11-01",
        end_date="2021-11-10",
    )

    assert rollout.value
