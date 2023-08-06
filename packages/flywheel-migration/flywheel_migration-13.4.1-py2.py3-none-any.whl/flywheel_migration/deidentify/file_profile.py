"""Individual file/packfile profile for de-identification"""

from abc import ABCMeta, abstractmethod
from dateutil.parser import parse
import fnmatch
import json
import logging
import os
import re

from flywheel_migration.deidentify.deid_field import (
    DeIdField,
    DeIdRegexSubField,
    DeIdIncrementDateField,
    DeIdIncrementDateTimeField,
    DeIdJitterField,
    DEFAULT_JITTER_TYPE,
)
import flywheel_migration.deidentify.validation as deid_validation
from flywheel_migration.util import sanitize_filename

log = logging.getLogger(__name__)


class FileProfile:
    # pylint: disable=too-many-public-methods
    """Abstract class that represents a single file/packfile profile"""
    __metaclass__ = ABCMeta

    # NOTE: If you derive from this class, set a unique name for the factory method to use
    name = None
    log_fields = []

    # NOTE: Date/Time formats are from dicom standard, override as necessary
    # http://dicom.nema.org/medical/dicom/current/output/chtml/part05/sect_6.2.html

    uid_default_prefix_fields = 4
    uid_default_suffix_fields = 1
    uid_max_suffix_digits = (
        6  # Maximum number of digits to keep from the suffix (trailing)
    )
    uid_hash_fields = (
        6,
        6,
        6,
        6,
        6,
        6,
    )  # The number and length of parts to add to the hash

    hash_digits = 0  # How many digits are supported for 'hash' action
    hash_algorithm = "sha256"
    date_format = "%Y%m%d"  # YYYYMMDD
    datetime_format = "%Y%m%d%H%M%S.%f"  # YYYYMMDDHHMMSS.FFFFFF&ZZXX
    datetime_has_timezone = True  # Whether or not optional timezone exists
    jitter_range = 2  # default range for jitter action
    jitter_type = (
        DEFAULT_JITTER_TYPE  # default type for jitter action ("int" or "float")
    )
    replace_with_insert = (
        True  # if True, insert data element with replace-with if it cans
    )

    default_filenames = []
    filename_field_prefix = "_fwmtk"

    # Allow for defining field with keyword 'regex' instead of 'name'
    regex_compatible = False

    deidfield_mixin = None

    sanitize_filename = True

    def __init__(self, packfile_type=None, file_filter=None):
        """Initialize the file profile"""
        self.packfile_type = packfile_type
        self.file_filter = file_filter
        self.fields = []
        self.field_map = {}
        self.log = None
        self.deid_name = None

        # Action configuration
        self.date_increment = None
        self.hash_salt = None

        self.uid_prefix_fields = (
            self.uid_default_prefix_fields
        )  # How many prefix nodes to keep
        self.uid_suffix_fields = (
            self.uid_default_suffix_fields
        )  # How many suffix nodes to keep
        self.uid_numeric_name = (
            None  # unique OID registered numeric name used as UID prefix if defined
        )

        self.filenames = self.default_filenames

    @classmethod
    def get_subclasses(cls):
        """Returns all subclasses (not the immediate ones only)"""
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass

    def add_field(self, field):
        """Add a field to de-identify"""
        if getattr(field, "_is_regex", None) and not self.regex_compatible:
            raise ValueError(
                f"regex in field is not compatible for profile {self.name}"
            )

        self.fields.append(field)
        self.field_map[field.fieldname] = field

    def has_field(self, var_fieldname):
        """
        Returns True if var_fieldname is defined in field_map or a regex field
            matches var_fieldname, else returns False
        """
        has_field = False
        if self.field_map.get(var_fieldname):
            has_field = True
        if not has_field and self.regex_compatible:
            for fieldname, field in self.field_map.items():
                if getattr(field, "_is_regex", None):
                    regexp = re.compile(fieldname)
                    if regexp.match(var_fieldname):
                        has_field = True
        return has_field

    def set_log(self, log):
        # pylint: disable=redefined-outer-name
        """Set the log instance"""
        if isinstance(log, list):
            self.log = log
        else:
            self.log = [log]

    def add_log(self, log):
        # pylint: disable=redefined-outer-name
        """Set the log instance"""
        if not self.log:
            self.set_log(log)
        else:
            self.log.append(log)

    def get_log_fields(self):
        """Return the full set of fieldnames that should be logged"""
        result = list(self.log_fields)  # predefined log fields
        for field in self.fields:
            if field.fieldname in result:  # in case field is in log_fields
                result[result.index(field.fieldname)] = field.fieldname
            else:
                result.append(field.fieldname)
        return result

    @classmethod
    def factory(cls, name, config=None, log=None):
        # pylint: disable=redefined-outer-name
        """Create a new file profile instance for the given name.

        Arguments:
            name (str): The name of the profile type
            config (dict): The optional configuration dictionary
            log: The optional de-id log instance
        """
        result = None

        for subclass in cls.get_subclasses():
            if subclass.name == name:
                result = subclass()
                break

        if not result:
            raise ValueError("Unknown file profile: '{}'".format(name))

        if config is not None:
            result.load_config(config)

        if log is not None:
            result.set_log(log)

        return result

    @classmethod
    def profile_names(cls):
        """Get the list of profile names"""
        result = []
        for subclass in cls.get_subclasses():
            if subclass.name is not None:
                result.append(subclass.name)

        return result

    def to_config(self):
        """Get configuration as a dictionary"""

        result = {"fields": [field.to_config() for field in self.fields]}

        # Read action configuration, explicit is better than implicit
        result["date-increment"] = self.date_increment
        result["salt"] = self.hash_salt
        result["uid-prefix-fields"] = self.uid_prefix_fields
        result["uid-suffix-fields"] = self.uid_suffix_fields
        result["uid-numeric-name"] = self.uid_numeric_name
        result["filenames"] = self.filenames
        result["file-filter"] = self.file_filter
        result["datetime-format"] = self.datetime_format
        result["date-format"] = self.date_format
        result["jitter-range"] = self.jitter_range
        result["jitter-type"] = self.jitter_type
        result["replace-with-insert"] = self.replace_with_insert
        result["hash-digits"] = self.hash_digits

        return result

    @staticmethod
    def sort_fields(field_list):
        """Sort field_list such that regex-sub fields are first"""
        new_field_list = list()
        for field in field_list:
            if "regex-sub" in field.keys():
                new_field_list.insert(0, field)
            else:
                new_field_list.append(field)
        return new_field_list

    def load_config(self, config):
        """Read configuration from a dictionary"""
        # Sort fields
        config["fields"] = self.sort_fields(config.get("fields", []))
        # Read fields
        for field in config.get("fields", []):
            self.add_field(DeIdField.factory(field, mixin=self.deidfield_mixin))

        # Read file_filter
        self.file_filter = config.get("file-filter", self.file_filter)

        # Read action configuration
        self.hash_digits = config.get("hash-digits", self.hash_digits)
        self.date_increment = config.get("date-increment", None)
        self.datetime_format = config.get("datetime-format", self.datetime_format)
        self.date_format = config.get("date-format", self.date_format)
        self.jitter_range = config.get("jitter-range", self.jitter_range)
        self.jitter_type = config.get("jitter-type", self.jitter_type)
        self.replace_with_insert = config.get(
            "replace-with-insert", self.replace_with_insert
        )
        self.hash_salt = config.get("salt", None)
        self.uid_prefix_fields = config.get(
            "uid-prefix-fields", self.uid_default_prefix_fields
        )
        self.uid_suffix_fields = config.get(
            "uid-suffix-fields", self.uid_default_suffix_fields
        )
        self.uid_numeric_name = config.get("uid-numeric-name", None)

        # Add fields for filenames
        self.filenames = config.get("filenames", self.default_filenames)
        if self.filenames:
            for i, filename in enumerate(self.filenames):
                if "groups" in filename:
                    for grp in filename.get("groups"):
                        grp_tmp = grp.copy()
                        grp_tmp[
                            "name"
                        ] = f'{self.filename_field_prefix}_filename{i}_{grp["name"]}'
                        self.add_field(
                            DeIdField.factory(
                                grp_tmp, dry=True, mixin=self.deidfield_mixin
                            )
                        )
                self._add_keep_fields(filename)

    def _add_keep_fields(self, filename):
        """Add keep field for certain keyword of filename.output

        Elements of filename['output'] that are not in, fields, groups or extracted from the
        filename['input-regexp'] are set as keep field"""
        regex = re.compile(r"\{([^}]+)\}")
        out_vars = regex.findall(filename.get("output"))
        regex = re.compile(filename.get("input-regex"))
        group_names = regex.groupindex.keys()
        for out_var in out_vars:
            if out_var not in self.field_map and out_var not in group_names:
                field_config = {"name": out_var, "keep": True}
                self.add_field(
                    DeIdField.factory(field_config, mixin=self.deidfield_mixin)
                )

    def matches_file(self, filename):
        """Check if this profile can process the given file"""
        if self.file_filter:
            if isinstance(self.file_filter, list):
                return any([fnmatch.fnmatch(filename, ff) for ff in self.file_filter])
            if isinstance(self.file_filter, str):
                return fnmatch.fnmatch(filename, self.file_filter)
            raise TypeError(
                f"Unrecognized type for profile file_filter ({type(self.file_filter)})"
            )
        return False

    def matches_packfile(self, packfile_type):
        """Check if this profile can process the given packfile"""
        return self.packfile_type and self.packfile_type == packfile_type

    def process_files(self, src_fs, dst_fs, files, callback=None):
        """Process all files in the file list, performing de-identification steps

        Args:
            src_fs: The source filesystem (Provides open function)
            dst_fs: The destination filesystem
            files: The set of files in src_fs to process
            callback: Function to call after writing each file
        """
        state = self.create_file_state()

        for path in files:
            # Load file
            record, modified = self.load_record(state, src_fs, path)

            # Record could be None if it should be skipped
            if record is None:
                continue

            # Set filenames attributes on record
            self.set_filenames_attributes(record, path)

            # Get destination path
            dst_path = self.get_dest_path(state, record, path)

            # Destination could be None if it should be skipped
            if not dst_path:
                continue

            if modified or self.fields:
                # Create before entry, if log is provided
                if self.log:
                    self.write_log_entry(path, "before", state, record)

                # De-identify
                for field in self.fields:
                    field.deidentify(self, state, record)

                # Create after entry, if log is provided
                if self.log:
                    self.write_log_entry(path, "after", state, record)

                # Save to dst_fs if we modified the record
                self.save_record(state, record, dst_fs, dst_path)
            else:
                # No fields to de-identify, just copy to dst
                with src_fs.open(path, "rb") as src_file:
                    dst_fs.upload(dst_path, src_file)

            if callable(callback):
                callback(dst_fs, dst_path)

    def get_value(self, state, record, fieldname):
        """Get the transformed value for fieldname"""
        field = self.field_map.get(fieldname)
        if field:
            return field.get_value(self, state, record)
        return self.read_field(state, record, fieldname)

    def create_file_state(self):  # pylint: disable=no-self-use
        """Create state object for processing files"""
        return None

    def get_dest_path(
        self, state, record, path
    ):  # pylint: disable=no-self-use, unused-argument
        """Get destination path"""
        if self.filenames:
            dest_path = None
            for i, filename in enumerate(self.filenames):
                format_kws = {}
                if "input-regex" in filename:
                    match = re.match(filename["input-regex"], path)
                    if not match:
                        continue
                    format_kws.update(match.groupdict())
                    key_mapping = {
                        k: f"{self.filename_field_prefix}_filename{i}_{k}"
                        for k in format_kws
                    }
                    for k in format_kws:
                        format_kws[k] = self.get_value(state, record, key_mapping[k])
                kws = [
                    x
                    for x in re.findall(r"\{([^}]+)\}", filename["output"])
                    if x not in format_kws
                ]
                for k in kws:
                    format_kws[k] = self.get_value(state, record, k)
                dest_path = filename["output"].format(**format_kws)
                break
            if dest_path is None:
                log.warning("IGNORING %s. No filename input-regex matches", path)
        else:
            dest_path = os.path.basename(path)

        if self.sanitize_filename:
            dest_path = sanitize_filename(dest_path)

        return dest_path

    def get_log_entry(self, path, entry_type, state, record):
        """Returns a dictionary with key/value corresponding to log entry and the logged fields"""
        fieldnames = self.get_log_fields()
        logged_fields = {}

        log_entry = {"path": path, "type": entry_type}
        for fieldname in fieldnames:
            if fieldname in self.field_map:
                field = self.field_map[fieldname]
                logged_fields[fieldname] = field
                if not fieldname.is_flat or field.is_regex:
                    fns = field.list_fieldname(record)
                    # In case of non-flat fieldname (e.g. regex, repeater)
                    # list_fieldname returns all matching data element paths for
                    # the record and log_entry value is a key/value dict for these
                    # data elements
                    log_entry_field = {}
                    for fn in fns:
                        log_entry_field[fn] = self.read_field(state, record, fn)
                    log_entry[fieldname] = json.dumps(log_entry_field)
                else:
                    log_entry[fieldname] = self.read_field(state, record, fieldname)
            else:
                log_entry[fieldname] = self.read_field(state, record, fieldname)

        return log_entry, logged_fields

    def write_log_entry(self, path, entry_type, state, record):
        """Write a single log entry of type for path"""
        log_entry, logged_fields = self.get_log_entry(path, entry_type, state, record)
        for logger in self.log:
            logger.write_entry(
                log_entry,
                path=path,
                entry_type=entry_type,
                state=state,
                record=record,
                logged_fields=logged_fields,
            )

    def validate(self, enhanced=False):
        # pylint: disable=unused-argument
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): Performed a deeper validation if supported

        Returns:
            list(str): A list of error messages, or an empty list
        """
        errors = []

        # validate date-format and datetime-format settings
        if self.date_format:
            errors += deid_validation.validate_datetime_format_code(self.date_format)
        if self.datetime_format:
            errors += deid_validation.validate_datetime_format_code(
                self.datetime_format
            )

        if self.filenames:
            for filename in self.filenames:
                if filename.get("input-regex"):  # check regexp
                    try:
                        _ = re.compile(filename.get("input-regex", ""))
                    except re.error:
                        errors.append(
                            f"Regex in deid profile is invalid: {filename.get('input-regex')}"
                        )

        if self.uid_numeric_name:
            errors += deid_validation.validate_uid_numeric_name(
                self.uid_numeric_name, self.uid_prefix_fields
            )

        if self.jitter_range:
            deid_validation.validate_jitter(self.jitter_range, self.jitter_type)

        # validate fields
        for fieldname, field in self.field_map.items():
            if isinstance(field, DeIdIncrementDateTimeField):
                if field.datetime_format is not None:
                    errors += deid_validation.validate_datetime_format_code(
                        field.datetime_format
                    )

            if isinstance(field, DeIdIncrementDateField):
                if field.date_format is not None:
                    errors += deid_validation.validate_datetime_format_code(
                        field.date_format
                    )

            if isinstance(field, DeIdRegexSubField):
                for member in field.list_members:
                    errors += deid_validation.validate_regexsubfield_member(member)

            if isinstance(field, DeIdJitterField):
                if field.jitter_range is not None:
                    errors += deid_validation.validate_jitter(
                        field.jitter_range, field.jitter_type
                    )

        return errors

    def _process_filename_groups(self, format_kws, groups):
        """Returning a processed group dict

        Args:
            format_kws (dict): Dictionary of group/value from a regex match
            groups (list): List of group (filename field-like) element

        Return:
            (dict): A processed group dict with key=<group name>/value=<processed value>
        """
        # convert group with increment-date action to expected date or datetime format
        for k, v in format_kws.items():
            for grp in groups:
                if grp["name"] == k:
                    if "increment-date" in grp:
                        date_format = grp.get("date-format", self.date_format)
                        format_kws[k] = parse(v).strftime(date_format)
                    elif "increment-datetime" in grp:
                        datetime_format = grp.get(
                            "datetime-format", self.datetime_format
                        )
                        format_kws[k] = parse(v).strftime(datetime_format)
        return format_kws

    def set_filenames_attributes(self, record, path):
        r"""Update record object with private attributes based on filenames properties

        Record attributes are extended based on <groups> extracted from the <input-regex>.
        For instance the following filenames schema defines in profile::

            filenames:
                - output: {group1}.ext
                  input-regex=r'^(?P<group1>[\w]+).ext$'
                - output: {group1}-{group2}.ext
                  input-regex=r'^(?P<group1>[\w]+)-(?P<date1>[\d]+).ext$'

        will create attributes, depending on which input-regex matches, as::

            # for `path` = test.ext
            record.<self.filename_field_prefix>_filename0_group1 = 'test'
            # for `path` = test-20200130.ext
            record.<self.filename_field_prefix>_filename1_group1 = 'test'
            # for `path` = test-20200130.ext
            record.<self.filename_field_prefix>_filename1_date1 = '20200130'

        Args:
            record (object): A record
            path (str): basename of input file
        """
        if self.filenames:
            filenames_attrs = {}
            for i, filename in enumerate(self.filenames):
                if "input-regex" in filename:
                    match = re.match(filename["input-regex"], path)
                    if not match:
                        continue
                    format_kws = match.groupdict()
                    if "groups" in filename:
                        format_kws = self._process_filename_groups(
                            format_kws, filename["groups"]
                        )
                    format_kws = {
                        f"{self.filename_field_prefix}_filename{i}_{k}": v
                        for k, v in format_kws.items()
                    }

                    filenames_attrs.update(format_kws)

            # update record with filenames attributes
            if filenames_attrs:
                for k, v in filenames_attrs.items():
                    setattr(record, k, v)

    def __deepcopy__(self, memodict=None):
        return FileProfile.factory(
            name=self.name, config=self.to_config(), log=self.log
        )

    @abstractmethod
    def load_record(self, state, src_fs, path):
        """Load the record(file) at path, return None to ignore this file"""

    @abstractmethod
    def save_record(self, state, record, dst_fs, path):
        """Save the record to the destination path"""

    @abstractmethod
    def read_field(self, state, record, fieldname):
        """Read the named field as a string. Return None if field cannot be read."""

    @abstractmethod
    def remove_field(self, state, record, fieldname):
        """Remove the named field from the record"""

    @abstractmethod
    def replace_field(self, state, record, fieldname, value):
        """Replace the named field with value in the record"""
