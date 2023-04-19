import sys
import re
import datetime as dt
import zoneinfo as zi

from typing import cast

import click


def make_datetime(date_time: str, timezone: zi.ZoneInfo) -> dt.datetime:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2}) (\d{1,2}):(\d{2})$",
                     date_time)

    if match is None:
        raise ValueError(
            f"Date and time '{date_time}' does not match format "
            + "YYYY-MM-DD HH:MM.")

    return dt.datetime(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        int(match.group(5)),
        tzinfo=timezone)


def format_datetime(obj: dt.datetime) -> str:
    tz_name = obj.tzname()
    tz_key = cast(zi.ZoneInfo, obj.tzinfo).key

    return f"{tz_name}: {obj.strftime('%Y-%m-%d %H:%M')} ({tz_key})"


@click.command()
@click.option("-d", "--debug", is_flag=True)
@click.option("-f", "--from-tz", required=True, type=str)
@click.option("-t", "--to-tz", required=True, type=str, multiple=True)
@click.argument("date_time", type=str)
def main(from_tz, to_tz, date_time, debug=False):
    if not debug:
        sys.tracebacklimit = 0

    from_tz_obj = zi.ZoneInfo(from_tz)
    to_tz_objs = [zi.ZoneInfo(x) for x in to_tz]

    base_dt = make_datetime(date_time, from_tz_obj)

    print(format_datetime(base_dt))

    for timezone in to_tz_objs:
        print(
            format_datetime(
                base_dt.astimezone(timezone)))


if __name__ == "__main__":
    main()
