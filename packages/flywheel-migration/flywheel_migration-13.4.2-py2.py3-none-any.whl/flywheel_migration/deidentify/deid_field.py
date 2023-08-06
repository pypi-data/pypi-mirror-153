"""Represents action to take in order to de-id a single field"""
import copy
import logging
import random
import re
import warnings

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

from flywheel_migration import util

log = logging.getLogger(__name__)
# Example: +0000 (Dicom), +00:00 (datetime)
RE_TIMEZONES = [re.compile(r"(.+)([-+]\d{4})$"), re.compile(r"(.+)([-+]\d{2}:\d{2})$")]
RE_OUTPUT = re.compile(r"\{([^}]+)\}")
DEFAULT_JITTER_TYPE = "float"
UID_MAX_LENGTH = 64


class DeIdFieldMixin:
    """Mixin base class to add functionalities to DeIdField based on profile used"""

    __metaclass__ = ABCMeta
    flavor = None  # to be used as prefix for the DeIdField subclasses name


class DeIdField:
    """Abstract class that represents action to take to de-identify a single field"""

    __metaclass__ = ABCMeta

    # NOTE: If you derive from this class, set a unique key for the factory method to use
    key = None
    __hash_cache = {}

    _props = {}

    def __init__(
        self,
        fieldname,
        is_regex=False,
        dry=False,
    ):
        self.fieldname = fieldname
        self._is_regex = is_regex
        self._dry = dry  # if True, does not modify record

    def __str__(self):
        return f"{self.__class__.__name__}: {self.fieldname}"

    def __repr__(self):
        return self.__str__()

    @property
    def is_dry(self):
        return self._dry

    @property
    def is_regex(self):
        return self._is_regex

    def list_fieldname(self, record):
        """Return a list of fieldnames for record.

        By default returns [self.fieldname]. Can be overwritten by certain
        subclasses of FieldEnhancerBaseMixin to returns a range of record attributes
        (e.g. when field uses regex, or range definition).
        """
        return [self.fieldname]

    @classmethod
    def factory(cls, config, dry=False, mixin=None):
        """Create a new DeIdField instance for the given config.

        Arguments:
            config (dict): The field configuration
            dry (bool): Is set to true, set the field as dry, i.e. a field that does not
                modify the record.
            mixin (DeIdFieldMixin): Optional subclass of DeIdFieldMixin to be
                inherited by the DeIdField subclass to make the field profile specific.
        """
        result = None
        is_regex = False
        name = config.get("name")
        regex = config.get("regex")
        if name and regex:
            raise ValueError(
                f"Field can not have name and regex defined. " f"Both found in {config}"
            )
        if name:
            fieldname = name
        elif regex:
            fieldname = regex
            is_regex = True
        else:
            raise ValueError(
                f"Field element must defined either name or regex. "
                f"none found in {config}"
            )

        deidfield_class = cls.get_deidfield_class(config)

        if deidfield_class is None:
            raise ValueError("Unknown de-identify action")
        else:
            if mixin:
                # Attach a mixin (DeIdFieldMixin subclass) to the deidfield_class
                # Use to "flavor" the deidfield_class adding features to DeIdField
                # such as support for "regex", etc.
                subclass_name = f"{mixin.flavor}{cls.__name__}"
                deidfield_class = type(subclass_name, (mixin, deidfield_class), {})

            result = deidfield_class(
                fieldname,
                is_regex=is_regex,
                dry=dry,
            )

        result.load_config(config)
        return result

    @classmethod
    def get_deidfield_class(cls, config):
        """Returns DeIdField subclass matching config.

        If only "name" is defined in config, returns DeIdKeepField, otherwise returns
        DeIdField subclass based on key action found in config.

        Args:
            config (dict): Dictionary e.g. {"name": "PatientID", "replace-with": "TOTO"}

        Returns:
            DeIdField or None: A DeIdField subclass or None if none is matching config
        """
        if list(config.keys()) == ["name"]:  # default action is keep
            return DeIdKeepField
        else:
            for subclass in cls.__subclasses__():
                for key in config.keys():
                    if subclass.key == key:
                        return subclass
        return None

    def to_config(self):
        """Convert to configuration dictionary"""
        result = {}
        if self._is_regex:
            result["regex"] = str(self.fieldname)
        else:
            result["name"] = str(self.fieldname)
        self.local_to_config(result)
        return result

    def local_to_config(self, config):
        """Convert rule specific settings to configuration dictionary"""
        # Most fields just store True in the key field
        config[self.key] = True

    def load_config(self, config):
        """Load rule specific settings from configuration dictionary"""

    def deidentify(self, profile, state, record):
        """Perform the update - default implementation is to do a replace"""
        if not self.is_dry:
            new_value = self.get_value(profile, state, record)
            if new_value is not None:
                profile.replace_field(state, record, self.fieldname, new_value)

    @abstractmethod
    def get_value(self, profile, state, record):
        """Get the transformed value, given profile state and record"""

    @classmethod
    def _hash(cls, profile, value, output_format="hex"):
        """Hash a value according to profile rules"""
        # Memoize hash results
        salt = profile.hash_salt
        hash_key = (salt, value, output_format)
        result = cls.__hash_cache.get(hash_key)
        if not result:
            result = util.hash_value(
                value,
                algorithm=profile.hash_algorithm,
                salt=salt,
                output_format=output_format,
            )
            cls.__hash_cache[hash_key] = result
        return result

    def _perform_date_inc(self, profile, state, record, fmt, timezone=False):
        new_value = None
        original = profile.read_field(state, record, self.fieldname)
        if original:
            suffix = ""

            # NOTE: Parsing optional timezone doesn't seem to be universally supported
            # Since we don't actually need the value, just strip and reapply if present
            if timezone:
                for tz_reg in RE_TIMEZONES:
                    match = tz_reg.match(original)
                    if match:
                        original = match.group(1)
                        suffix = match.group(2)
                        break
            # Add fractional seconds to datetime string if they are not present
            if fmt.endswith(".%f") and "." not in original:
                original = original + ".0"
            # TODO: Should we capture ValueError here?
            try:
                orig_date = datetime.strptime(original, fmt)
                new_date = orig_date + timedelta(days=profile.date_increment)
                new_value = new_date.strftime(fmt) + suffix
            except ValueError as err:
                log.error(
                    "NO ACTION WAS TAKEN! Unable to parse date field: %s\n%s",
                    self.fieldname,
                    err,
                )

        return new_value

    def _jitter(self, profile, state, record, jitter_range, jitter_type):
        """Return a randomly jittered value"""
        new_value = None
        original = profile.read_field(state, record, self.fieldname)
        if original is not None:
            # cast to numeric
            try:
                if jitter_type == "int":
                    original = int(original)
                else:
                    original = float(original)
            except ValueError as err:
                log.error(
                    "NO ACTION WAS TAKEN! Unable to cast jitter field to numeric: %s\n%s",
                    self.fieldname,
                    err,
                )

            if jitter_range == 0:
                # sanity check, should be captured upon profile validation
                raise ValueError("jitter-range cannot be 0")

            # get random value
            rand_val = 0
            while not rand_val:
                if jitter_type == "int":
                    rand_val = random.randint(-int(jitter_range), int(jitter_range))
                else:
                    rand_val = random.uniform(-1, 1) * jitter_range

            try:
                new_value = original + rand_val
            except (TypeError, ValueError) as err:
                log.error(
                    "NO ACTION WAS TAKEN! Unable to jitter field: %s\n%s",
                    self.fieldname,
                    err,
                )

        return new_value


class DeIdIdentityField(DeIdField):
    """Action to do nothing on a field. Same as keep action. To be deprecated."""

    key = "identity"

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "'identity' action will be deprecated in version 14, use 'keep' action instead",
            PendingDeprecationWarning,
        )
        super(DeIdIdentityField, self).__init__(*args, **kwargs)

    def deidentify(self, profile, state, record):
        """Do nothing

        Use in fieldname section, regex-sub and with remove-undefined action.
        """
        pass

    def get_value(self, profile, state, record):
        return profile.read_field(state, record, self.fieldname)


class DeIdKeepField(DeIdField):
    """Action to do nothing on a field"""

    key = "keep"

    def deidentify(self, profile, state, record):
        """Do nothing.

        Use in fieldname section, regex-sub and with remove-undefined action.
        """
        pass

    def get_value(self, profile, state, record):
        return profile.read_field(state, record, self.fieldname)


class DeIdRemoveField(DeIdField):
    """Action to remove a field from the record"""

    key = "remove"

    def deidentify(self, profile, state, record):
        profile.remove_field(state, record, self.fieldname)

    def get_value(self, profile, state, record):
        return None


class DeIdReplaceField(DeIdField):
    """Action to replace a field from the record"""

    key = "replace-with"

    def __init__(self, fieldname, **kwargs):
        super(DeIdReplaceField, self).__init__(fieldname, **kwargs)
        self.replace_with_insert = None
        self.value = None

    def get_value(self, profile, state, record):
        replace_with_insert = self.replace_with_insert
        if replace_with_insert is None:
            replace_with_insert = profile.replace_with_insert

        original = profile.read_field(state, record, self.fieldname)
        if original is None and replace_with_insert is False:
            # returns None so that value is not changed
            return None

        return self.value

    def local_to_config(self, config):
        super(DeIdReplaceField, self).local_to_config(config)
        config["replace-with"] = self.value
        config["replace-with-insert"] = self.replace_with_insert

    def load_config(self, config):
        self.value = config[self.key]
        if "replace-with-insert" in config:
            self.replace_with_insert = config.get("replace-with-insert")


class DeIdHashField(DeIdField):
    """Action to replace a field with it's hashed value"""

    key = "hash"

    def get_value(self, profile, state, record):
        new_value = None
        original = profile.read_field(state, record, self.fieldname)
        if original:
            new_value = self._hash(profile, original)

            # Respect character limit, if applicable
            if profile.hash_digits > 0:
                new_value = new_value[: profile.hash_digits]

        return new_value


class DeIdHashUIDField(DeIdField):
    """Action to replace a uid field with it's hashed value"""

    key = "hashuid"

    def get_value(self, profile, state, record):
        new_value = None

        original = profile.read_field(state, record, self.fieldname)
        if original:
            orig_parts = original.split(".")

            # Determine how many fields are required
            if not profile.uid_numeric_name:
                required = profile.uid_prefix_fields + profile.uid_suffix_fields
                if required > len(orig_parts):
                    raise ValueError("UID is too short to be hashed")

            # Get the digest
            digest = self._hash(profile, original, output_format="dec")
            result_parts = []

            # Build the new UID string with prefix
            if profile.uid_prefix_fields > 0:
                if profile.uid_numeric_name:
                    if (
                        not len(profile.uid_numeric_name.split("."))
                        == profile.uid_prefix_fields
                    ):
                        raise ValueError(
                            f"Registered OID numeric name must have exactly {profile.uid_prefix_fields} "
                            f"fields"
                        )
                    result_parts += profile.uid_numeric_name.split(".")
                else:
                    result_parts += orig_parts[: profile.uid_prefix_fields]

            # Parts taken from hash string
            idx = 0
            for seg in profile.uid_hash_fields:
                # Workaround for avoiding E203:
                #   https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-398693703
                to_index = idx + seg
                part = digest[idx:to_index]
                if part[0] == "0":
                    # DICOM UID block cannot start with 0, replacing by 1
                    part = f"1{part[1:]}"
                result_parts.append(part)
                idx += seg

            # And suffix
            if profile.uid_suffix_fields > 0:
                suffix = []
                # Keep no more than the number of digits specified
                # i.e. strip any dates
                # Workaround for avoiding E203:
                #   https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-398693703
                from_index = -profile.uid_suffix_fields
                for part in orig_parts[from_index:]:
                    if len(part) > profile.uid_max_suffix_digits:
                        # Workaround for avoiding E203:
                        #   https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-398693703
                        from_index_max_suffix_digits = -profile.uid_max_suffix_digits
                        part = part[from_index_max_suffix_digits:]
                    suffix.append(part)
                result_parts += suffix

            new_value = ".".join(result_parts)

            # crop to stay within UID_MAX_LENGTH for dicom compliance
            if len(new_value) > UID_MAX_LENGTH:
                parts = new_value.split(".")
                rest, suffix = parts[:-1], parts[-1]
                while len(".".join(rest)) + 1 + len(suffix) > UID_MAX_LENGTH:
                    if len(rest[-1]) > 1:
                        rest[-1] = rest[-1][:-1]
                    else:
                        _ = rest.pop(-1)
                rest.append(suffix)
                new_value = ".".join(rest)

        return new_value


class DeIdIncrementDateField(DeIdField):
    """Action to replace a field with it's incremented date"""

    key = "increment-date"

    def __init__(self, fieldname, **kwargs):
        super(DeIdIncrementDateField, self).__init__(fieldname, **kwargs)
        self.date_format = None

    def load_config(self, config):
        if "date-format" in config:
            self.date_format = config.get("date-format")

    def get_value(self, profile, state, record):
        date_format = self.date_format if self.date_format else profile.date_format
        return self._perform_date_inc(profile, state, record, date_format)

    def local_to_config(self, config):
        super(DeIdIncrementDateField, self).local_to_config(config)
        if self.date_format:
            config["date-format"] = self.date_format


class DeIdJitterField(DeIdField):
    """Action to jitter a field with some random number from a uniform distribution on
    a range"""

    key = "jitter"

    def __init__(self, fieldname, **kwargs):
        super(DeIdJitterField, self).__init__(fieldname, **kwargs)
        self.jitter_range = None
        self.jitter_type = DEFAULT_JITTER_TYPE

    def load_config(self, config):
        if "jitter-range" in config:
            self.jitter_range = config.get("jitter-range")
        if "jitter-type" in config:
            self.jitter_type = config.get("jitter-type")

    def get_value(self, profile, state, record):
        jitter_range = self.jitter_range
        if jitter_range is None:
            jitter_range = profile.jitter_range

        jitter_type = self.jitter_type
        if jitter_type is None:
            jitter_type = profile.jitter_type

        return self._jitter(profile, state, record, jitter_range, jitter_type)

    def local_to_config(self, config):
        super(DeIdJitterField, self).local_to_config(config)
        if self.jitter_range:
            config["jitter-range"] = self.jitter_range
        if self.jitter_type:
            config["jitter-type"] = self.jitter_type


class DeIdIncrementDateTimeField(DeIdField):
    """Action to replace a field with it's incremented date"""

    key = "increment-datetime"

    def __init__(self, fieldname, **kwargs):
        super(DeIdIncrementDateTimeField, self).__init__(fieldname, **kwargs)
        self.datetime_format = None

    def load_config(self, config):
        if "datetime-format" in config:
            self.datetime_format = config.get("datetime-format")

    def get_value(self, profile, state, record):
        datetime_format = (
            self.datetime_format if self.datetime_format else profile.datetime_format
        )
        return self._perform_date_inc(
            profile, state, record, datetime_format, timezone=True
        )

    def local_to_config(self, config):
        super(DeIdIncrementDateTimeField, self).local_to_config(config)
        if self.datetime_format:
            config["datetime-format"] = self.datetime_format


class DeIdRegexSubField(DeIdField):
    """Action to edit a string matching a regex with capture groups"""

    key = "regex-sub"

    def __init__(self, fieldname, **kwargs):
        super(DeIdRegexSubField, self).__init__(fieldname, **kwargs)
        self.list_members = list()
        self.input_regex = None
        self.output_regex = re.compile(r"\{([^}]+)\}")
        self.output = None

    @staticmethod
    def _patch_profile(profile, read_value):
        """
        Create a copy of the FileProfile, replacing read_field with a function
            that returns read_value
        """
        from flywheel_migration.deidentify.file_profile import FileProfile

        def _patched_read_field(*args):  # pylint: disable=unused-argument
            return read_value

        new_profile = FileProfile.factory(
            profile.name, config=profile.to_config(), log=profile.log
        )
        new_profile.read_field = _patched_read_field
        return new_profile

    def load_config(self, config):
        for item in config.get(self.key):
            self.list_members.append(DeIdRegexSubListItem(item))

    def local_to_config(self, config):
        config[self.key] = [member.to_config() for member in self.list_members]
        return config

    def get_value(self, profile, state, record):
        current = profile.read_field(state, record, self.fieldname)
        # Don't attempt regex-sub if current value is None
        if current is None:
            return None
        match = False
        for member in self.list_members:
            if member.regex_matches_field_value(current):
                match = True
                break
        if match is False:
            raise ValueError(
                f"Field {self.fieldname} value {current} does not match any of the input-regex values"
            )
        out_vars = self.output_regex.findall(member.output)
        val_dict = dict()
        for var_name in out_vars:
            match = member.input_regex.match(current)
            match_val = match.groupdict().get(var_name)
            if member.group_dict.get(var_name):
                group_field = member.group_dict.get(var_name)
                if match_val is not None:
                    patch_profile = self._patch_profile(profile, match_val)
                    var_value = group_field.get_value(patch_profile, state, record)
                else:
                    if (
                        profile.field_map.get(var_name)
                        and group_field.key != "identity"
                        and group_field.key != "keep"
                    ):
                        warn_str = (
                            f"Field {var_name} is defined in the profile AND in"
                            f" a {self.fieldname} group. Group action will be"
                            " applied after profile action."
                        )
                        log.warning(warn_str)
                    var_value = group_field.get_value(profile, state, record)
            elif match_val is not None:
                var_value = match_val
            else:
                err_str = (
                    f"Action for {var_name} is not defined in groups for "
                    f"{member.input_regex}. Please modify "
                    f"profile for {self.fieldname}"
                )
                raise ValueError(err_str)

            if var_value is None:
                var_value = ""
            val_dict[var_name] = var_value

        return member.format_output(val_dict)


class DeIdRegexSubListItem:
    """Class for representing a list item within DeIdRegexSubField"""

    output_dot_replace_char = "___"

    def __init__(self, config):
        self.input_regex = re.compile(config.get("input-regex"))
        self.group_dict = dict()
        self._preprocess_output(config.get("output"))
        self.output_vars = RE_OUTPUT.findall(self.output)
        self._load_group_config(config.get("groups", []))

    def _preprocess_output(self, output):
        """Create mapping to allow for referencing variable with '.' in output"""
        self.output = output

        # output referencing dotty key (e.g. '{label}_{subject.label}') cannot be
        # formatted readily because `.` is an object attribute delimiter.
        output_map = {}
        proc_output = output
        for var in re.findall(r"\{([^}]+)\}", output):
            if "." in var:
                xmap = var.replace(".", self.output_dot_replace_char)
                output_map[var] = xmap
                proc_output = proc_output.replace(var, xmap)
            else:
                output_map[var] = var
        self._output_map = output_map
        self._proc_output = proc_output

    def format_output(self, val_dict):
        """Format output according to output_map"""
        val_dict_mapped = {self._output_map[k]: v for k, v in val_dict.items()}
        return self._proc_output.format(**val_dict_mapped)

    def _load_group_config(self, group_list):
        """Load the configuration for the groups"""
        for group_config in group_list:
            group_member_field = DeIdField.factory(group_config, dry=True)
            self.group_dict[group_member_field.fieldname] = group_member_field

    def regex_matches_field_value(self, value):
        """return True if the value matches the regex, else False"""
        return bool(self.input_regex.match(value))

    def to_config(self):
        """Convert to configuration dictionary"""
        config_dict = dict()
        config_dict["input-regex"] = self.input_regex.pattern
        config_dict["output"] = self.output
        config_dict["groups"] = [
            group.to_config() for group in self.group_dict.values()
        ]
        return config_dict

    def is_capture_group(self, var_name):
        """
        Return True if the varname matches a named capture group in
            self.input_regex
        """
        return bool(self.input_regex.groupindex.get(var_name))

    def var_name_is_valid(self, var_name):
        """
        Return True if the varname is a capture group or is defined in self.group_dict,
        False otherwise.
        """
        valid = False
        if self.is_capture_group(var_name):
            valid = True
        if self.group_dict.get(var_name):
            valid = True

        return valid

    def get_invalid_output_vars(self):
        """Return a list of invalid output_vars"""
        invalid_vars = [
            var for var in self.output_vars if not self.var_name_is_valid(var)
        ]
        return invalid_vars
