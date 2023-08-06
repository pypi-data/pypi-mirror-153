"""Contains classes to represent complex elements of an IOS Shell file."""
from dataclasses import dataclass
import datetime
from typing import Any, Dict, List

EMPTY = ["", "' '", "n/a"]
NAN = float("NaN")


@dataclass
class Version:
    """Represents the \\*IOS HEADER VERSION line of the file."""

    version_no: str
    date1: str
    date2: str
    tag: str = ""


class Channel:
    """A single entry in the CHANNELS table."""

    no: int  # acts as an identifier
    name: str
    units: str
    minimum: float
    maximum: float

    def __init__(
        self,
        no="",
        name="",
        units="",
        minimum="",
        maximum="",
    ):
        self.no = int(no)
        self.name = name.strip()
        self.units = units.strip()
        # FIXME: remove when no longer relevant
        if minimum.strip().upper() == "O":
            minimum = "0"
        if maximum.strip().upper() == "O":
            maximum = "0"
        self.minimum = float(minimum) if minimum.strip() not in EMPTY else NAN
        self.maximum = float(maximum) if maximum.strip() not in EMPTY else NAN


class ChannelDetail:
    """A single entry in the CHANNEL DETAILS table."""

    no: int  # acts as an identifier
    pad: float
    start: str
    width: int
    format: str
    type: str
    decimal_places: int = -1

    def __init__(
        self,
        no="",
        pad="",
        start="",
        width="",
        format="",
        type="",
        decimal_places="",
    ):
        self.no = int(no)
        self.pad = float(pad) if pad.strip() not in EMPTY else NAN
        self.start = start
        self.width = int(width) if width.strip() not in EMPTY else 0
        self.format = format
        self.type = type
        self.decimal_places = (
            int(decimal_places) if decimal_places.strip() not in EMPTY else 0
        )


@dataclass
class FileInfo:
    """Represents the \\*FILE section."""

    start_time: datetime.datetime
    end_time: datetime.datetime
    time_zero: datetime.datetime
    time_increment: datetime.timedelta
    time_units: str
    number_of_records: int
    data_description: str
    file_type: str
    format: str
    data_type: str
    pad: float
    number_of_channels: int
    channels: List[Channel]
    channel_details: List[ChannelDetail]
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Administration:
    """Represents the \\*ADMINISTRATION section."""

    mission: str
    agency: str
    country: str
    project: str
    scientist: str
    platform: str
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Location:
    """Represents the \\*LOCATION section."""

    geographic_area: str
    station: str
    event_number: int
    latitude: float
    longitude: float
    water_depth: float
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Instrument:
    """Represents the \\*INSTRUMENT section."""

    type: str
    model: str
    serial_number: str
    depth: float
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Program:
    """A single entry in the PROGRAMS table."""

    name: str
    version: str
    date: datetime.date
    time: datetime.time
    records_in: int
    records_out: int


@dataclass
class Raw:
    """Represents the \\*RAW section."""

    remarks: str
    raw: Dict[str, Any]


@dataclass
class History:
    """Represents the \\*HISTORY section."""

    programs: List[Program]
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Calibration:
    """Represents the \\*CALIBRATION section."""

    corrected_channels: List[Dict[str, str]]
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Deployment:
    """Represents the \\*DEPLOYMENT section."""

    mission: str
    type: str
    anchor_dropped: datetime.datetime
    remarks: str
    raw: Dict[str, Any]


@dataclass
class Recovery:
    """Represents the \\*RECOVERY section."""

    mission: str
    anchor_released: datetime.datetime
    remarks: str
    raw: Dict[str, Any]
