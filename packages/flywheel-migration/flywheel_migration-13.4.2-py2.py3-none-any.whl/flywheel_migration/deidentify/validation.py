"""A set a functions to validate certain profile/field attribute"""
from _strptime import TimeRE
import re

DT_CODES = [f"%{k}" for k in TimeRE().keys()]
DT_FORMAT_RE = re.compile(r"%\w")

# OID for Flywheel Migration Toolkit (unmanaged sub-zones)
# Flywheel Dicom UID Management Plan is defined in:
# https://docs.google.com/document/d/1HcMcWBrDsYIFOkMgGL8W7Hzt7I2tl4UbeC40R5HH99A
FW_OID_ROOT = "2.16.840.1.114570"
FW_OID_MTK_ROOT = "2.16.840.1.114570.2.2"


def validate_datetime_format_code(dt_format):
    """Validate the date/datetime format, returning any errors

    Args:
        df_format (str): The date or datetime format (e.g. %Y%m%d)

    Returns:
        list: List of error messages, or an empty list
    """
    errors = []
    if dt_format:
        for f in DT_FORMAT_RE.findall(dt_format):
            if f not in DT_CODES:
                errors.append(f"{f} is not a supported datetime format code")
    return errors


def validate_jitter(jitter_range, jitter_type):
    """Validate the jitter_range, returning any errors

    Args:
        jitter_range (float or int): The jitter-range

    Returns:
        list: List of error messages, or an empty list
    """
    errors = []
    if jitter_range == 0:
        errors.append(f"jitter-range cannot be 0")

    if jitter_type == "int" and jitter_range < 1:
        errors.append(f"jitter-range cannot be < 1 when jitter-type is {jitter_type}")

    return errors


def validate_regexsubfield_member(member):
    """Validate the RegexSubField member, returning any errors

    Args:
        member (flywheel_migration.deidentify.deid_field.DeIdRegexSubListItem): A RegexSubField memeber

    Returns:
        list: List of error messages, or an empty list
    """
    errors = []
    invalid_fields = member.get_invalid_output_vars()
    if invalid_fields:
        errors.append(
            f"{member.input_regex} contains "
            "group members that are not capture groups and do"
            " not have de-id action defined: "
            f"{str(invalid_fields)}"
        )
    return errors


def validate_uid_numeric_name(uid_numeric_name, uid_prefix_fields):
    """Validate uid_numeric_name, returning any errors

    Args:
        uid_numeric_name (str): A string representing the uid_numeric_name

    Returns:
        list: List of error messages, or an empty list
    """
    errors = []
    if uid_numeric_name.startswith(FW_OID_ROOT):
        if not uid_numeric_name == FW_OID_MTK_ROOT:
            errors.append(
                f"uid_numeric_name used Flywheel root OID but does not conform to "
                f"Flywheel DICOM UID Management Plan. Please use: {FW_OID_MTK_ROOT}"
            )
    if not len(uid_numeric_name.split(".")) == uid_prefix_fields:
        errors.append(
            f"uid_prefix_fields is different from number of blocks in uid_numeric_name. "
            f"They must matches. Currently at "
            f'{uid_prefix_fields}/{len(uid_numeric_name.split("."))} '
            f"respectively"
        )

    return errors
