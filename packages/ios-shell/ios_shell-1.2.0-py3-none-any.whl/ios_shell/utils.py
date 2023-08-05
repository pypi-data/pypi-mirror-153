"""Contains useful functions for parsing that are not themselves parsing functions."""
import datetime
from typing import List, Any

from .regex import *


def apply_column_mask(data: str, mask: str) -> List[str]:
    """Apply a mask to a single row of data.

    :param data: the row of data to break up
    :param mask: a string with '-' for every character to be included as an element
    """
    data = data.ljust(len(mask))
    end = 0
    out = []
    while end > -1:  # pragma: no mutate
        start = mask.find("-", end)  # pragma: no mutate
        end = mask.find(" ", start)
        out.append(data[start:end])
    out[-1] += data[end:]
    return out


def format_string(format: str, kind: str, width: int, decimals: int) -> str:
    """Construct an appropriate format string for the given type.

    :param format: the format the data is expected to conform to
    :param kind: the type the data is expected to be
    :param width: the number of characters the data may take up
    :param decimals: the number of characters after a decimal a float is intended to use
    """
    fortrantype = format.strip().upper()
    datatype = kind.strip().upper()
    if datatype in ["DT"]:
        return f"A17"
    elif fortrantype in ["F"]:
        return f"F{width}.{decimals}"
    elif fortrantype in ["E"]:
        return f"E{width}.{decimals}"
    elif fortrantype in ["I"]:
        return f"I{width}"
    elif fortrantype.upper() in [
        "YYYY/MM/DD",
        "YYYY-MM-DD",
        "HH:MM",
        "HH:MM:SS",
        "HH:MM:SS.SS",
    ]:
        return f"A{len(fortrantype)+1}"
    elif fortrantype in ["' '", "NQ"]:
        return f"A{width}"
    else:
        return fortrantype


def _to_timezone_offset(name: str) -> int:
    upper = name.upper()
    if upper in ["UTC", "GMT"]:
        return 0
    elif upper in ["ADT"]:
        return -3
    elif upper in ["MDT", "CST"]:
        return -6
    elif upper in ["PDT", "MST"]:
        return -7
    elif upper in ["PST"]:
        return -8
    else:
        raise ValueError(f"Unknown time zone: {name}.")


def to_date(contents: str) -> datetime.date:
    """Convert a string representing a date into a usable object."""
    date_info = [int(part) for part in contents.strip().replace("-", "/").split("/")]
    year = date_info[0]
    month = date_info[1]
    day = date_info[2]
    return datetime.date(year, month, day)


def to_time(contents: str, tzinfo=datetime.timezone.utc) -> datetime.time:
    """Convert a string representing a time into a usable object."""
    time_info = [
        int(part) for piece in contents.strip().split(":") for part in piece.split(".")
    ]
    hour = time_info[0]
    minute = time_info[1]
    second = time_info[2] if len(time_info) > 2 else 0
    return datetime.time(hour=hour, minute=minute, second=second, tzinfo=tzinfo)


def _to_datetime(tz: str, date: str, time: str) -> datetime.datetime:
    tzoffset = _to_timezone_offset(tz)
    date_obj = to_date(date)
    tz_obj = datetime.timezone(datetime.timedelta(hours=tzoffset))
    if time != "":
        time_obj = to_time(time, tz_obj)
        return datetime.datetime.combine(date_obj, time_obj)
    else:
        return datetime.datetime(
            date_obj.year, date_obj.month, date_obj.day, tzinfo=tz_obj
        )


def to_datetime(value: str) -> datetime.datetime:
    """Convert a string representing a date and time into a usable object."""
    # attempting to cover "Unknown" and "Unk.000"
    if value in ["", "?"] or "unk" in value.lower():
        return datetime.datetime.min
    trimmed = value.strip()
    # separate matches are required in order to avoid reusing group names
    if m := DATE_TIME_PATTERN.match(trimmed):
        return _to_datetime(tz="UTC", **m.groupdict())
    elif m := TZ_DATE_TIME_PATTERN.match(trimmed):
        return _to_datetime(**m.groupdict(""))
    elif m := DATE_TIME_TZ_PATTERN.match(trimmed):
        return _to_datetime(**m.groupdict(""))
    else:
        raise ValueError(f"Unknown time format: {value}")


def to_increment(description: str) -> datetime.timedelta:
    if description == "n/a":
        return datetime.timedelta(seconds=0)
    days, hours, minutes, seconds, mseconds = description.split(" ")
    return datetime.timedelta(
        days=float(days),
        hours=float(hours),
        minutes=float(minutes),
        seconds=float(seconds),
        milliseconds=float(mseconds),
    )


def _get_coord(raw_coord: str, positive_marker: str, negative_marker: str) -> float:
    coord = raw_coord.split("!")[0]
    degrees, minutes, direction = coord.split()
    out = float(degrees) + float(minutes) / 60.0
    if direction.upper() == positive_marker.upper():
        return out
    elif direction.upper() == negative_marker.upper():
        return out * -1.0  # pragma: no mutate
    else:
        raise ValueError("Coordinate contains unknown direction marker")


def get_latitude(coord: str) -> float:
    """Convert a string representing a latitude into a floating point number."""
    return _get_coord(coord, "N", "S")


def get_longitude(coord: str) -> float:
    """Convert a string representing a longitude into a floating point number."""
    return _get_coord(coord, "E", "W")


def is_section_heading(s: str) -> bool:
    """Decide whether or not a string represents the beginning of a secion."""
    return SECTION_HEADING_PATTERN.fullmatch(s) is not None


def is_table_mask(line: str) -> bool:
    """Decide whether or not a string is a table mask.

    A table mask starts with an indentation, then a '!' character, and then a mixture
    of ' ' and '-'
    """
    return (
        line.startswith(" ")
        and line.lstrip().startswith("!")
        and "-" in line
        and all(c in [" ", "!", "-"] for c in line)
    )


def has_many_values(list: List[Any]) -> bool:
    """Decide whether or not a list has more than one value"""
    return len(list) > 1


def all_same(list: List[Any]) -> bool:
    """Decide whether or not a list's values are all the same"""
    return len(set(list)) == 1


def list_to_pandas(list: List[List[Any]], names: List[str]):
    """Convert list of lists to pandas DataFrame

    :param list: the data as a list of data rows
    :param names: the row names to be used in the pandas.DataFrame
    :return: a pandas.DataFrame if pandas is present, otherwise None
    """
    try:
        import pandas
    except ImportError:
        return None  # pragma: no mutate

    df = pandas.DataFrame(list)
    return df.rename(columns=lambda old: names[old])
