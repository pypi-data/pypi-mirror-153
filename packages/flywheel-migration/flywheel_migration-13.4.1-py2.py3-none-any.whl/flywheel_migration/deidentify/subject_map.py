"""Provides base class for SubjectMap implementations"""
from abc import ABCMeta, abstractmethod
import warnings

SUBJECT_LABEL_KEY = "SubjectCode"


class SubjectMapConfig:
    """Configuration for subject mapping"""

    def __init__(self, fields, format_str):
        """Create the subject map config

        Arguments:
            fields (list): The ordered list of fields to use as a key
            format_str (str): The format string (e.g. 'ex{SubjectCode:02}')
        """
        self._fields = fields
        self._format_str = format_str

    @property
    def fields(self):
        """Return the list of fields used when mapping subjects"""
        return self._fields

    @property
    def format_str(self):
        """Return the format string used when mapping subjects"""
        return self._format_str

    def format_label(self, label):
        """Format numeric subject label using format_str"""
        format_args = {SUBJECT_LABEL_KEY: label}
        return self._format_str.format(**format_args)

    def format_code(self, code):
        """Backward-compatibility #FLYW-3539."""
        warnings.warn(
            "'code' attribute is deprecated now. Use 'label'", DeprecationWarning
        )
        return self.format_label(code)


class SubjectMap:
    """Abstract base class for mapping subjects to labels"""

    __metaclass__ = ABCMeta

    """Provides subject mapping functionality"""

    def __init__(self):
        self.config = None

    def get_config(self):
        """Return the configuration for this SubjectMap"""
        return self.config

    def get_label(self, record):
        """Given a record, get the subject label

        Args:
            record: A dictionary-like object containing fields to be mapped

        Returns:
            str: The formatted subject label
        """
        label = self.lookup_label(record)
        return self.config.format_label(label)

    def get_code(self, record):
        """Backward-compatibility #FLYW-3539."""
        warnings.warn(
            "'code' attribute is deprecated now. Use 'label'", DeprecationWarning
        )
        return self.get_label(record)

    def lookup_label(self, record):
        """
        Because of backward compatibility (#FLYW-3539) this method calls the lookup_code which
        remains the abstact one.
        Only in case of major version change this can overtake the lookup_code completly.
        """
        return self.lookup_code(record)

    @abstractmethod
    def lookup_code(self, record):
        """Lookup subject label for the given record

        Args:
            record: A dictionary-like object containing fields to be mapped

        Returns:
            int: The numeric subject label
        """

    @abstractmethod
    def load(self):
        """Load the subject map from disk"""

    @abstractmethod
    def save(self):
        """Save the subject map to disk"""

    @abstractmethod
    def rows(self):
        """Generator that returns all of the rows in the subject map, as dictionaries"""

    @staticmethod
    def extract_field(record, fieldname):
        """Extract field from record, and normalize it (by converting to lowercase and stripping whitespace)

        Args:
            record: A dictionary-like object
            fieldname (str): The field to extract

        Returns:
            str: The normalized value
        """
        value = record.get(fieldname, "")
        return str(value).strip().lower()
