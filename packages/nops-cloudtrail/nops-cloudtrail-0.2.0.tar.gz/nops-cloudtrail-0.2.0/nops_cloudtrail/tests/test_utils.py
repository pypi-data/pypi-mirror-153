from datetime import datetime

from nops_cloudtrail.utils import day_chunks


def test_day_chunks():
    start = datetime(year=2001, month=3, day=1, hour=1, minute=15)
    end = datetime(year=2001, month=4, day=3, hour=10, minute=30)

    chunks = list(day_chunks(start=start, end=end))

    assert chunks

    first_chunk = chunks.pop(0)
    assert first_chunk[0] == start
    last_chunk = chunks.pop()
    assert last_chunk[1] == end

    for _start, _end in chunks:
        # assert _start.date() == _end.date()
        assert _start.hour == 0
        assert _start.minute == 0
        assert _start.second == 0
        assert _start.microsecond == 0

        assert _end.hour == 23
        assert _end.minute == 59
        assert _end.second == 59
        assert _end.microsecond == 999999
