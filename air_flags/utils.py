import random
from datetime import datetime
from typing import List


def calc_progressive_percentage(
    percentage: int,
    start_date: str,
    end_date: str,
    max_value: int,
    date_format: str,
) -> int:
    if datetime.today() < datetime.strptime(
        start_date, date_format
    ) or datetime.today() > datetime.strptime(end_date, date_format):
        return 0

    period = datetime.strptime(end_date, date_format) - datetime.strptime(
        start_date, date_format
    )
    multiplier = (max_value - percentage) / period.days
    now = datetime.today() - datetime.strptime(start_date, date_format)
    increment = multiplier * now.days
    progressive_percentage = percentage + increment

    return int(progressive_percentage)


def generate_random_value(
    choices: List, percentage: int, max_value: int
) -> bool:
    return random.choices(choices, [percentage, max_value - percentage])[0]
