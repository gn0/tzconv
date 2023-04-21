import sys
import re
import datetime as dt
import zoneinfo as zi

from typing import cast

import click


def make_datetime(date_time: str, timezone: zi.ZoneInfo) -> dt.datetime:
    """Construct a `datetime` instance from a date-time string formatted
    as `YYYY-MM-DD HH:MM` or `HH:MM` and attach timezone information."""

    match = (
        re.match(r"^\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}):(\d{2})\s*$",
                 date_time)
        or re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", date_time)
    )

    if match is None:
        raise ValueError(
            f"Date and time '{date_time}' matches neither "
            + "'YYYY-MM-DD HH:MM' nor 'HH:MM'.")

    if len(match.groups()) == 5:
        year, month, day, hour, minute = tuple(int(x)
                                               for x in match.groups())
    else:
        today = dt.date.today()

        year, month, day = today.year, today.month, today.day
        hour, minute = tuple(int(x) for x in match.groups())

    return dt.datetime(year, month, day, hour, minute, tzinfo=timezone)


def format_datetime(obj: dt.datetime) -> str:
    """Create a human-readable representation of a `datetime`
    object. The resulting string includes the timezone's name and its
    `zoneinfo` key."""

    tz_name = obj.tzname()
    tz_key = cast(zi.ZoneInfo, obj.tzinfo).key

    return f"{tz_name}: {obj.strftime('%Y-%m-%d %H:%M')} ({tz_key})"


def print_time_zones(stub):
    """Print all available time zones whose names begin with `stub`.  If
    `stub` is `None`, then print everything."""

    time_zones = zi.available_timezones()

    if stub is not None:
        time_zones = set(
            x
            for x in time_zones
            if x.lower().startswith(stub.lower()))

        if len(time_zones) == 0:
            print(f"No available time zone begins with '{stub}'.")
            return

        print("The following time zones are available that begin with "
            + f"'{stub}':\n")
    else:
        print("The following time zones are available:\n")

    chars_on_line = 0

    for index, time_zone in enumerate(sorted(time_zones)):
        if index + 1 < len(time_zones):
            output_string = f" {time_zone},"
        else:
            output_string = f" {time_zone}\n"

        if chars_on_line == 0:
            print(" ", end="")

        if (chars_on_line == 0
            or chars_on_line + len(output_string) <= 78):
            print(output_string, end="")

            chars_on_line += len(output_string)
        else:
            print(f"\n {output_string}", end="")

            chars_on_line = len(output_string)


def print_argument_error_and_exit(message: str) -> None:
    """Print an error message, show the help message, and exit."""

    print(f"Error: {message}\n", file=sys.stderr)

    context = click.get_current_context()

    click.echo(context.get_help())
    context.exit()


@click.command(help=("Convert a date and time from one time zone to "
                     + "one or more other time zones."))
@click.option("-d", "--debug", is_flag=True)
@click.option("-l", "--list-tz", is_flag=True,
              help=("List all available time zones. The list can be "
                    + "narrowed by providing the beginning of the name "
                    + "of the time zone, e.g., 'Af', as an additional "
                    + "argument."))
@click.option("-f", "--from-tz", required=False, type=str,
              help="The name of the time zone to convert from.")
@click.option("-t", "--to-tz", required=False, type=str, multiple=True,
              help=("The name of a time zone to convert to. Can use "
                    + "this option multiple times in order to specify "
                    + "several."))
@click.argument("date_time", required=False, type=str)
def main(from_tz, to_tz, date_time, list_tz=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0

    if list_tz:
        if from_tz is not None or len(to_tz) > 0:
            print_argument_error_and_exit(
                "--list-tz cannot be used together with --from-tz or "
                "--to-tz.")

        print_time_zones(date_time)
    elif from_tz is None and len(to_tz) == 0:
        print_argument_error_and_exit(
            "Must specify either --list-tz or --from-tz and --to-tz.")
    elif from_tz is None:
        print_argument_error_and_exit(
            "Must specify --from-tz if using --to-tz.")
    elif len(to_tz) == 0:
        print_argument_error_and_exit(
            "Must specify --to-tz if using --from-tz.")
    elif date_time is None:
        print_argument_error_and_exit(
            "Must specify a date and time to convert.")
    else:
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
