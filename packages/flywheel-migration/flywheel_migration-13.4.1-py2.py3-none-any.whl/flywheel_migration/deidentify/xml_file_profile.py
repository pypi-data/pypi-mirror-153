"""File profile for de-identifying XML files"""
import types
import logging
import re

from lxml import etree
from dateutil.parser import parse

from .file_profile import FileProfile
from .deid_field import DeIdField

log = logging.getLogger(__name__)

XPATH_RE = re.compile(r"(^\/.+)|(^\.\/.+)")  # to enforce XPath to start with / or ./


def parse_fieldname(name):
    """Parse the given string to determine if it's XPath compatible.

    Params:
        name (str): The XPath expression

    Returns:
        XPathStr
    """
    try:
        # Test XPath compliance
        _ = etree.XPath(name)
        # Test
        match = XPATH_RE.match(name)
        if match:
            return XPathStr(name, is_xpath=True, original=name)
    except (etree.XPathSyntaxError, etree.XPathEvalError):
        pass
    return XPathStr(name)


class XMLRecord:  # pylint: disable=too-few-public-methods
    """A record for dealing with XML file

    This is a dump class to allow for storing arbitrary attributes because lxml.etree._ElementTree does
    not allow for it (inheritance from a custom Class object that seems to prohibit it)
    """

    def __init__(self, fp):
        self.tree = etree.parse(fp)

    def save_as(self, fp):
        """Save xml tree"""
        self.tree.write(fp)


class XPathStr(str):
    """Subclass of string with a few extra attributes related to xml"""

    def __new__(cls, value, *_args, **_kwargs):
        return super(XPathStr, cls).__new__(cls, value)

    def __init__(self, _value, is_xpath=False, original=None):
        super(XPathStr, self).__init__()
        self._is_xpath = is_xpath
        self._original = original


class XMLFileProfile(FileProfile):
    """Exif implementation of load/save and remove/replace fields"""

    name = "xml"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = []
    record_class = XMLRecord
    default_file_filter = ["*.XML", "*.xml"]

    def __init__(self, file_filter=None):
        file_filter = file_filter if file_filter else self.default_file_filter
        super(XMLFileProfile, self).__init__(
            packfile_type=self.name, file_filter=file_filter
        )

    def create_file_state(self):
        """Create state object for processing files"""
        return {}

    def load_record(self, state, src_fs, path):
        modified = False
        try:
            with src_fs.open(path, "r") as f:
                record = self.record_class(f)
        except Exception:  # pylint: disable=broad-except
            log.warning("IGNORING %s - it is not a %s file!", path, self.name)
            return None, False

        return record, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "wb") as f:
            record.save_as(f)

    def add_field(self, field):
        """Add field to profile"""
        field.fieldname = parse_fieldname(field.fieldname)

        def deidentify_list(field, profile, state, record):
            els = record.tree.xpath(field.fieldname)
            for el in els:
                fieldname = XPathStr(
                    record.tree.getpath(el), is_xpath=True, original=field.fieldname
                )
                tmp_field = DeIdField.factory(
                    {"name": fieldname, field.key: getattr(field, "value", True)}
                )
                tmp_field.deidentify(profile, state, record)

        xpath = getattr(field.fieldname, "_is_xpath", False)
        if xpath:
            field.deidentify = types.MethodType(deidentify_list, field)

        super(XMLFileProfile, self).add_field(field)

    def read_field(self, state, record, fieldname):
        """Read field from record"""
        xpath = getattr(fieldname, "_is_xpath", None)
        if xpath:
            res = record.tree.xpath(fieldname)
            if len(res) > 1:
                raise ValueError(f"xpath ({fieldname}) returned more than one element")
            if not res:
                value = None
            else:
                value = res[0].text
        else:
            value = getattr(record, fieldname, None)

        # format datetime on the fly
        original = (
            fieldname
            if not hasattr(fieldname, "_original")
            else getattr(fieldname, "_original")
        )
        if (
            original in self.field_map
        ):  # require for filenames manipulation without any field associated to it
            if (
                self.field_map[original].key in ["increment-datetime", "increment-date"]
                and value
            ):
                return parse(value).strftime(self.datetime_format)

        return value

    def remove_field(self, state, record, fieldname):
        xpath = getattr(fieldname, "_is_xpath", None)
        if xpath:
            res = record.tree.xpath(fieldname)
            if len(res) > 1:
                raise ValueError(f"xpath ({fieldname}) returned more than one element")
            if len(res) == 1:
                res[0].getparent().remove(res[0])
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def replace_field(self, state, record, fieldname, value):
        xpath = getattr(fieldname, "_is_xpath", None)
        if xpath:
            res = record.tree.xpath(fieldname)
            if len(res) > 1:
                raise ValueError(f"xpath ({fieldname}) returned more than one element")
            if len(res) == 1:
                res[0].text = value
        else:
            setattr(record, fieldname, value)
