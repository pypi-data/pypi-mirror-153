"""Provides functions for scanning bruker parameters files"""
import datetime
import logging
import re

log = logging.getLogger(__name__)


def set_nested_attr(obj, key, value):
    """Set a nested attribute in dictionary, creating sub dictionaries as necessary.

    Arguments:
        obj (dict): The top-level dictionary
        key (str): The dot-separated key
        value: The value to set
    """
    parts = key.split(".")
    for part in parts[:-1]:
        obj.setdefault(part, {})
        obj = obj[part]
    obj[parts[-1]] = value


# pylint: disable=too-many-branches
def parse_bruker_params(fileobj):
    """Parse the pv5/6 parameters file, extracting keys

    References:
        - ParaVision D12_FileFormats.pdf
        - JCAMP DX format: http://www.jcamp-dx.org/protocols/dxnmr01.pdf

    Arguments:
        fileobj (file): The file-like object that supports readlines, opened in utf-8
    """
    result = {}

    # Variable names are ##/##$
    # And are either =value, =< value >, or =() with value(s) following the next lines
    # $$ appear to be comments

    key = None
    value = ""

    # Use regex to get ParaVision software version (also searching $$ comments)
    version_re = re.compile(r"(PV|ParaVision) ?(?P<version>\d+(\.\d+)+)")
    version = None

    for line in fileobj.readlines():
        if version is None:
            version_match = version_re.search(line)
            if version_match:
                result["PARAVISION_version"] = version = version_match.groupdict()[
                    "version"
                ]

        if line.startswith("$$"):
            continue

        try:
            if line.startswith("##"):
                if key:
                    result[key] = value

                # Parse parameter name
                key, _, value = line[2:].partition("=")
                key = key.lstrip(
                    "$"
                )  # Paravision uses private parameters prefixed with '$'
                value = value.strip()

                # Check value
                if not value:
                    continue

                # Case 1: value is wrapped in brackets: < foo >
                if value[0] == "<" and value[-1] == ">":
                    result[key] = value[1:-1].strip()
                    key = None
                    value = ""
                elif value[0] == "(":
                    # Case 2: value is a structure
                    if "," in value:
                        continue
                    # Case 3: value is size/dimensions, in which case we ignore it
                    value = ""
                    continue
                else:
                    # Case 4: value is directly assigned
                    result[key] = value.strip()
                    key = None
                    value = ""
            elif key:
                line = line.strip()
                if line[0] == "<" and line[-1] == ">":
                    line = line[1:-1]

                if value:
                    value = value + " "

                value = value + line
        except ValueError as ex:
            log.debug("Error processing bruker parameter line: %s", ex)
            # Any error should just reset state
            key = None
            value = ""

    if key:
        result[key] = value

    return result


def parse_bruker_epoch(abs_datetime):
    """Parse bruker parameter value containing an epoch (ie.: *_abs_date, *_abs_time).
    Arguments:
       abs_datetime (str): Bruker epoch value
    Returns:
       datetime.datetime: Datetime object in UTC
    """
    # Could be a tuple, e.g.: (352523325, 323, 43)
    if abs_datetime and abs_datetime[0] == "(":
        parts = abs_datetime.strip("()").split(",")
        abs_datetime = parts[0].strip()

    # Convert first part from seconds UTC
    try:
        return datetime.datetime.utcfromtimestamp(int(abs_datetime))
    except (ValueError, TypeError):
        return None
