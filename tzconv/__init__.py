import sys
import re
import datetime as dt
import zoneinfo as zi

import click


def make_datetime(date_time: str, tz: zi.ZoneInfo) -> dt.datetime:
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
        tzinfo=tz)


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

    from_tz_name = from_tz_obj.tzname(base_dt)

    print(f"{from_tz_name}: ", end="")
    print(f"{base_dt.strftime('%Y-%m-%d %H:%M')} ", end="")
    print(f"({from_tz})")

    for to_tz_obj in to_tz_objs:
        to_tz_name = to_tz_obj.tzname(base_dt)
        to_tz_dt = base_dt.astimezone(to_tz_obj)

        print(f"{to_tz_name}: ", end="")
        print(f"{to_tz_dt.strftime('%Y-%m-%d %H:%M')} ", end="")
        print(f"({to_tz_obj.key})")


if __name__ == "__main__":
    main()
