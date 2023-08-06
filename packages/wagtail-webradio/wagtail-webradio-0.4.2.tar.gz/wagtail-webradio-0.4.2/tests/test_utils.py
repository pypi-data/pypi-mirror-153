from datetime import timedelta

import pytest

from wagtail_webradio.utils import format_duration


@pytest.mark.parametrize(
    'duration, result',
    [
        (None, '--:--'),
        (timedelta(), '--:--'),
        (timedelta(seconds=2), '00:02'),
        (timedelta(minutes=3), '03:00'),
        (timedelta(minutes=12, seconds=10), '12:10'),
        (timedelta(hours=1, seconds=10), '01:00:10'),
    ],
)
def test_format_duration(duration, result):
    assert format_duration(duration) == result
