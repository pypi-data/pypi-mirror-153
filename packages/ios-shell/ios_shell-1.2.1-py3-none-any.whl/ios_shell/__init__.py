"""Read and process an IOS Shell file in Python."""

from .shell import ShellFile
from .sections import (
    Version,
    Channel,
    ChannelDetail,
    FileInfo,
    Administration,
    Location,
    Instrument,
    Program,
    Raw,
    History,
    Calibration,
    Deployment,
    Recovery,
)
