"""Contains functions for parsing files in IOS Shell format."""
import datetime
import fortranformat as ff
import itertools
import math
from typing import Any, Dict, List, Tuple

from . import sections, utils
from .regex import *
from .keys import *


def _next_line(rest: List[str]) -> Tuple[str, List[str]]:
    return rest[0], rest[1:]


def _has_key_prefix(line: str) -> bool:
    idx = line.find(":")
    key = line[:idx]
    return idx > 0 and key == key.upper()


def get_modified_date(contents: List[str]) -> Tuple[datetime.datetime, List[str]]:
    """Parse the modified date."""
    line, rest = _next_line(contents)
    if m := MODIFIED_DATE_PATTERN.fullmatch(line):
        return (utils.to_datetime(m.group(1)), rest)
    else:
        raise ValueError("No modified date at start of string")


def get_header_version(contents: List[str]) -> Tuple[sections.Version, List[str]]:
    """Parse the header version string."""
    line, rest = _next_line(contents)
    if m := HEADER_VERSION_PATTERN.fullmatch(line):
        return (sections.Version(**m.groupdict()), rest)
    else:
        raise ValueError("No header version in string")


def get_section(
    contents: List[str], section_name: str
) -> Tuple[Dict[str, Any], List[str]]:
    """Parse a named section."""
    line, rest = _next_line(contents)
    if line != "*" + section_name.upper():
        raise ValueError(
            f"{section_name.upper()} section not present, found {line} instead"
        )
    section_info: Dict[str, Any] = {}
    last_key = None
    indent_level = 0  # pragma: no mutate
    while not utils.is_section_heading(rest[0]):
        line, rest = _next_line(rest)
        current_indent_level = len(
            list(itertools.takewhile(lambda c: c in [" "], line))
        )
        if line.strip() == "" or line.startswith("!"):
            # skip comments
            if utils.is_table_mask(line):
                raise ValueError(
                    f"'{line}' is a table mask, but the table header was not found."
                )
        elif m := TABLE_START_PATTERN.fullmatch(line):
            # handle table
            table_name = m.group(1).lower()
            # table column names
            column_names_lines = []
            line, rest = _next_line(rest)
            # column names may appear across multiple lines
            while not utils.is_table_mask(line):
                if not line.lstrip().startswith("!"):
                    raise ValueError(
                        f"'{line}' was expected to contain the column names for the table {table_name}."
                    )
                column_names_lines.append(line)
                line, rest = _next_line(rest)
            mask = line

            raw_column_names: List[List[str]] = []
            for column_names_line in column_names_lines:
                # apply column mask in case names contain spaces
                names = utils.apply_column_mask(column_names_line, mask)
                raw_column_names.append([])
                for name in names:
                    raw_column_names[-1].append(name.lower().strip())
            # combine the column names from each row
            column_names = [
                " ".join(lines).strip().replace(" ", "_")
                for lines in zip(*raw_column_names)
            ]

            # values
            section_info[table_name] = []
            line, rest = _next_line(rest)
            while not END_PATTERN.fullmatch(line.lstrip()):
                section_info[table_name].append(
                    {
                        column_names[i]: v
                        for i, v in enumerate(utils.apply_column_mask(line, mask))
                    }
                )
                line, rest = _next_line(rest)
            last_key = None
        elif m := ARRAY_START_PATTERN.fullmatch(line):
            array_name = m.group(1).lower()
            section_info[array_name] = []
            line, rest = _next_line(rest)
            while not END_PATTERN.fullmatch(line):
                section_info[array_name].append(line)
                line, rest = _next_line(rest)
            last_key = None
        elif m := REMARKS_START_PATTERN.fullmatch(line):
            # handle remarks
            remarks = []
            line, rest = _next_line(rest)
            while not END_PATTERN.fullmatch(line):
                remarks.append(line)
                line, rest = _next_line(rest)
            section_info[REMARKS] = "\n".join(remarks)  # pragma: no mutate
            last_key = None
        elif _has_key_prefix(line):
            # handle single entry
            key, value = line.split(":", 1)
            last_key = key.strip().lower()
            section_info[last_key] = value.strip()
            indent_level = current_indent_level
        elif last_key is not None and current_indent_level > indent_level:
            # handle entry continuation
            section_info[last_key] += f" {line.strip()}"
        else:
            raise ValueError(f"Unexpected text: '{line}'")
    return section_info, rest


def get_file(contents: List[str]) -> Tuple[sections.FileInfo, List[str]]:
    """Parse the \\*FILE section."""
    file_dict, rest = get_section(contents, "file")
    start_time = (
        utils.to_datetime(file_dict[START_TIME])
        if START_TIME in file_dict
        else datetime.datetime.min
    )
    end_time = (
        utils.to_datetime(file_dict[END_TIME])
        if END_TIME in file_dict
        else datetime.datetime.min
    )
    time_zero = (
        utils.to_datetime(file_dict[TIME_ZERO])
        if TIME_ZERO in file_dict
        else datetime.datetime.min
    )
    time_increment = (
        utils.to_increment(file_dict[TIME_INCREMENT].split("!")[0].strip())
        if TIME_INCREMENT in file_dict
        else datetime.timedelta(seconds=0)
    )
    time_units = file_dict[TIME_UNITS] if TIME_UNITS in file_dict else ""
    number_of_records = int(file_dict[NUMBER_OF_RECORDS])
    data_description = (
        file_dict[DATA_DESCRIPTION] if DATA_DESCRIPTION in file_dict else "n/a"
    )
    file_type = file_dict[FILE_TYPE] if FILE_TYPE in file_dict else "n/a"
    number_of_channels = int(file_dict[NUMBER_OF_CHANNELS])
    channels = (
        [sections.Channel(**elem) for elem in file_dict[CHANNELS]]
        if CHANNELS in file_dict
        else []
    )
    channel_details = (
        [sections.ChannelDetail(**elem) for elem in file_dict[CHANNEL_DETAIL]]
        if CHANNEL_DETAIL in file_dict
        else []
    )
    data_type = file_dict[DATA_TYPE] if DATA_TYPE in file_dict else "n/a"
    to_remove = " \n\t'"  # pragma: no mutate
    if FORMAT in file_dict:
        format_str = file_dict[FORMAT].strip(to_remove)
        if CONTINUED in file_dict:
            format_str += file_dict[CONTINUED].strip(to_remove)
    else:
        format_info = [
            utils.format_string(
                detail.format, detail.type, detail.width, detail.decimal_places
            )
            for detail in channel_details
        ]
        format_str = "({})".format(",".join(format_info))
    pad = float(file_dict[PAD]) if PAD in file_dict else math.nan
    remarks = file_dict[REMARKS] if REMARKS in file_dict else ""
    file_info = sections.FileInfo(
        start_time=start_time,
        end_time=end_time,
        time_zero=time_zero,
        time_increment=time_increment,
        time_units=time_units,
        number_of_records=number_of_records,
        data_description=data_description,
        file_type=file_type,
        format=format_str,
        data_type=data_type,
        pad=pad,
        number_of_channels=number_of_channels,
        channels=channels,
        channel_details=channel_details,
        remarks=remarks,
        raw=file_dict,
    )
    return file_info, rest


def get_administration(
    contents: List[str],
) -> Tuple[sections.Administration, List[str]]:
    """Parse the \\*ADMINISTRATION section."""
    admin_dict, rest = get_section(contents, "administration")
    mission = admin_dict[MISSION] if MISSION in admin_dict else "n/a"
    agency = admin_dict[AGENCY] if AGENCY in admin_dict else "n/a"
    country = admin_dict[COUNTRY] if COUNTRY in admin_dict else "n/a"
    project = admin_dict[PROJECT] if PROJECT in admin_dict else "n/a"
    scientist = admin_dict[SCIENTIST] if SCIENTIST in admin_dict else "n/a"
    platform = admin_dict[PLATFORM] if PLATFORM in admin_dict else "n/a"
    remarks = admin_dict[REMARKS] if REMARKS in admin_dict else ""
    admin_info = sections.Administration(
        mission=mission,
        agency=agency,
        country=country,
        project=project,
        scientist=scientist,
        platform=platform,
        remarks=remarks,
        raw=admin_dict,
    )
    return admin_info, rest


def get_location(contents: List[str]) -> Tuple[sections.Location, List[str]]:
    """Parse the \\*LOCATION section"""
    location_dict, rest = get_section(contents, "location")
    geographic_area = (
        location_dict[GEOGRAPHIC_AREA] if GEOGRAPHIC_AREA in location_dict else "n/a"
    )
    station = location_dict[STATION] if STATION in location_dict else "n/a"
    event_number = (
        int(location_dict[EVENT_NUMBER]) if EVENT_NUMBER in location_dict else -1
    )
    latitude = utils.get_latitude(location_dict[LATITUDE])
    longitude = utils.get_longitude(location_dict[LONGITUDE])
    water_depth = (
        float(location_dict[WATER_DEPTH])
        if WATER_DEPTH in location_dict
        and location_dict[WATER_DEPTH].lower() not in ["", "unknown"]
        else -1
    )
    remarks = location_dict[REMARKS] if REMARKS in location_dict else ""
    location_info = sections.Location(
        geographic_area=geographic_area,
        station=station,
        event_number=event_number,
        latitude=latitude,
        longitude=longitude,
        water_depth=water_depth,
        remarks=remarks,
        raw=location_dict,
    )
    return location_info, rest


def get_instrument(contents: List[str]) -> Tuple[sections.Instrument, List[str]]:
    """Parse the \\*INSTRUMENT section"""
    instrument_dict, rest = get_section(contents, "instrument")
    kind = instrument_dict[TYPE] if TYPE in instrument_dict else "n/a"
    model = instrument_dict[MODEL] if MODEL in instrument_dict else "n/a"
    serial_number = (
        instrument_dict[SERIAL_NUMBER] if SERIAL_NUMBER in instrument_dict else "n/a"
    )
    depth = float(instrument_dict[DEPTH]) if DEPTH in instrument_dict else math.nan
    remarks = instrument_dict[REMARKS] if REMARKS in instrument_dict else ""
    instrument_info = sections.Instrument(
        type=kind,
        model=model,
        serial_number=serial_number,
        depth=depth,
        remarks=remarks,
        raw=instrument_dict,
    )
    return instrument_info, rest


def get_history(contents: List[str]) -> Tuple[sections.History, List[str]]:
    """Parse the \\*HISTORY section"""
    history_dict, rest = get_section(contents, "history")
    programs = (
        [sections.Program(*elem) for elem in history_dict[PROGRAMS]]
        if PROGRAMS in history_dict
        else []
    )
    remarks = history_dict[REMARKS] if REMARKS in history_dict else ""
    history_info = sections.History(
        programs=programs,
        remarks=remarks,
        raw=history_dict,
    )
    return history_info, rest


def get_calibration(contents: List[str]) -> Tuple[sections.Calibration, List[str]]:
    """Parse the \\*CALIBRATION section"""
    calibration_dict, rest = get_section(contents, "calibration")
    corrected_channels = (
        calibration_dict[CORRECTED_CHANNELS]
        if CORRECTED_CHANNELS in calibration_dict
        else []
    )
    remarks = calibration_dict[REMARKS] if REMARKS in calibration_dict else ""
    calibration_info = sections.Calibration(
        corrected_channels=corrected_channels,
        remarks=remarks,
        raw=calibration_dict,
    )
    return calibration_info, rest


def get_raw(contents: List[str]) -> Tuple[sections.Raw, List[str]]:
    """Parse the \\*RAW section"""
    raw_dict, rest = get_section(contents, "raw")
    remarks = raw_dict[REMARKS] if REMARKS in raw_dict else ""
    raw_info = sections.Raw(
        remarks=remarks,
        raw=raw_dict,
    )
    return raw_info, rest


def get_deployment(contents: List[str]) -> Tuple[sections.Deployment, List[str]]:
    """Parse the \\*DEPLOYMENT section"""
    deployment_dict, rest = get_section(contents, "deployment")
    mission = deployment_dict[MISSION] if MISSION in deployment_dict else "n/a"
    type = deployment_dict[TYPE] if TYPE in deployment_dict else "n/a"
    anchor_dropped = (
        utils.to_datetime(deployment_dict[TIME_ANCHOR_DROPPED])
        if TIME_ANCHOR_DROPPED in deployment_dict
        else datetime.datetime.min
    )
    remarks = deployment_dict[REMARKS] if REMARKS in deployment_dict else ""
    deployment_info = sections.Deployment(
        mission=mission,
        type=type,
        anchor_dropped=anchor_dropped,
        remarks=remarks,
        raw=deployment_dict,
    )
    return deployment_info, rest


def get_recovery(contents: List[str]) -> Tuple[sections.Recovery, List[str]]:
    """Parse the \\*RECOVERY section"""
    recovery_dict, rest = get_section(contents, "recovery")
    mission = recovery_dict[MISSION] if MISSION in recovery_dict else "n/a"
    anchor_released = (
        utils.to_datetime(recovery_dict[TIME_ANCHOR_RELEASED])
        if TIME_ANCHOR_RELEASED in recovery_dict
        else datetime.datetime.min
    )
    remarks = recovery_dict[REMARKS] if REMARKS in recovery_dict else ""
    recovery_info = sections.Recovery(
        mission=mission,
        anchor_released=anchor_released,
        remarks=remarks,
        raw=recovery_dict,
    )
    return recovery_info, rest


def get_comments(contents: List[str]) -> Tuple[str, List[str]]:
    """Parse the \\*COMMENTS section"""
    line, rest = _next_line(contents)
    if COMMENTS_START_PATTERN.fullmatch(line):
        lines = []
        while not utils.is_section_heading(rest[0]):
            line, rest = _next_line(rest)
            lines.append(line)
        return "\n".join(lines), rest
    else:
        raise ValueError("No COMMENTS section found")


def _has_date(contents: str) -> bool:
    return DATE_PATTERN.search(contents) is not None


def _has_time(contents: str) -> bool:
    return TIME_PATTERN.search(contents) is not None


def _process_item(contents: Any) -> Any:
    if not isinstance(contents, str):
        return contents
    has_date = _has_date(contents)
    has_time = _has_time(contents)
    if has_date and has_time:
        return utils.to_datetime(contents)
    elif has_date:
        return utils.to_date(contents)
    elif has_time:
        return utils.to_time(contents)
    else:
        return contents.strip()


def _postprocess_line(line: List[Any]) -> List[Any]:
    return [_process_item(item) for item in line]


def get_data(contents: str, format: str, records: int) -> Tuple[List[List[Any]], str]:
    """Process the data in the file"""
    lines = contents.splitlines()
    while "" in lines:
        lines.remove("")
    if len(lines) < records:
        raise ValueError(f"Insufficient data for requested number of records")
    reader = ff.FortranRecordReader(format)
    data = [_postprocess_line(reader.read(line)) for line in lines[:records]]
    rest = "\n".join(lines[records:])  # pragma: no mutate
    return data, rest
