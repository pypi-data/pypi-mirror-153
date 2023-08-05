"""This module holds constants for expected keys for each section in an IOS Shell file.

It exists because it is easier to ensure consistent string values by using constants instead of raw strings.
This also means typos are easier to correct.
"""

# common to all sections
REMARKS = "remarks"

# *FILE keys
START_TIME = "start time"
END_TIME = "end time"
TIME_ZERO = "time zero"
TIME_INCREMENT = "time increment"
TIME_UNITS = "time units"
NUMBER_OF_RECORDS = "number of records"
DATA_DESCRIPTION = "data description"
FILE_TYPE = "file type"
DATA_TYPE = "data type"
NUMBER_OF_CHANNELS = "number of channels"
CHANNELS = "channels"
CHANNEL_DETAIL = "channel detail"
FORMAT = "format"
CONTINUED = "continued"
PAD = "pad"

# *ADMINISTRATION keys
MISSION = "mission"
AGENCY = "agency"
COUNTRY = "country"
PROJECT = "project"
SCIENTIST = "scientist"
PLATFORM = "platform"

# *LOCATION keys
GEOGRAPHIC_AREA = "geographic area"
STATION = "station"
EVENT_NUMBER = "event number"
LATITUDE = "latitude"
LONGITUDE = "longitude"
WATER_DEPTH = "water depth"

# *INSTRUMENT keys
TYPE = "type"
MODEL = "model"
SERIAL_NUMBER = "serial number"
DEPTH = "depth"

# *HISTORY keys
PROGRAMS = "programs"

# *CALIBRATION keys
CORRECTED_CHANNELS = "corrected channels"

# *DEPLOYMENT keys
TIME_ANCHOR_DROPPED = "time anchor dropped"

# *RECOVERY keys
TIME_ANCHOR_RELEASED = "time anchor released"
