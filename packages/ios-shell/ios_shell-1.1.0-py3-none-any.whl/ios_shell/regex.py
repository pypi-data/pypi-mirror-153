"""This module holds constants for compiled regular expressions to be used in other modules.

Because there are so many regular expressions used with all sorts of access patterns, the internal
cache of regular expressions in re.match seems to be beyond its limit.
"""
import re


# common date and time patterns
DATE_STR = r"\d{4}[/-]\d{2}[/-]\d{2}"
DATE_PATTERN = re.compile(DATE_STR)
TIME_STR = r"\d{2}:\d{2}(:\d{2}(.\d*)?)?"
TIME_PATTERN = re.compile(TIME_STR)


# used in utils.py
TIMEZONE_STR = r"[A-Za-z]{3}"

# the names inside the < and > must be the same as the arguments to utils._to_datetime()
MATCH_DATE = f"(?P<date>{DATE_STR})"
MATCH_TZ = f"(?P<tz>{TIMEZONE_STR})"
MATCH_TIME = f"(?P<time>{TIME_STR})"

DATE_TIME_PATTERN = re.compile(f"{MATCH_DATE} {MATCH_TIME}")
TZ_DATE_TIME_PATTERN = re.compile(f"{MATCH_TZ} {MATCH_DATE}( {MATCH_TIME})?")
DATE_TIME_TZ_PATTERN = re.compile(f"{MATCH_DATE}( {MATCH_TIME})? {MATCH_TZ}")

SECTION_HEADING_PATTERN = re.compile(r"\*[A-Z ]+")


# used in parsing.py
MODIFIED_DATE_PATTERN = re.compile(rf"\*({DATE_STR} {TIME_STR})")

# the names inside the < and > must be the same as the arguments to sections.Version.__init__()
MATCH_VERSION = r"(?P<version_no>\d+.\d+)"
MATCH_DATE1 = f"(?P<date1>{DATE_STR})"
MATCH_DATE2 = f"(?P<date2>{DATE_STR})"
MATCH_TAG = "(?P<tag>[a-zA-Z0-9.]+)"

HEADER_VERSION_PATTERN = re.compile(
    rf"\*IOS HEADER VERSION +{MATCH_VERSION} +{MATCH_DATE1}( +{MATCH_DATE2}( +{MATCH_TAG})?)?"
)

TABLE_START_PATTERN = re.compile(r"\s*\$TABLE: (.+)")
ARRAY_START_PATTERN = re.compile(r"\s*\$ARRAY: (.+)")
REMARKS_START_PATTERN = re.compile(r"\s*\$REMARKS?")
END_PATTERN = re.compile(r"\s*\$END")

COMMENTS_START_PATTERN = re.compile(r"\*COMMENTS")

END_OF_HEADER_PATTERN = re.compile(r"\*END OF HEADER")
