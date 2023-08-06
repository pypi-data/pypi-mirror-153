"""File profile for de-identifying JSON/JSON file"""
import logging
import json
import re
import types

from dotty_dict import Dotty

from flywheel_migration.deidentify.file_profile import FileProfile
from flywheel_migration.deidentify.deid_field import DeIdField

log = logging.getLogger(__name__)


class JSONRecord:
    """A record for dealing with json file"""

    file_type = "JSON"
    default_separator = "."

    def __init__(self, fp, data=None, separator=None):
        if not separator:
            separator = self.default_separator
        if fp:
            self._metadata = Dotty(json.load(fp), separator=separator)
        elif data:
            self._metadata = Dotty(data, separator=separator)
        else:
            raise ValueError("Either fp or data must be defined.")

    def __getitem__(self, key):
        try:
            return self._metadata[key]
        except KeyError:  # looking for attribute on record (e.g. filename attribute)
            return getattr(self, key)

    def __setitem__(self, key, value):
        self._metadata[key] = value

    def __delitem__(self, key):
        self._metadata.pop(key)

    def __len__(self):
        return len(self._metadata)

    @property
    def separator(self):
        """Returns separator used in Dotty"""
        return self._metadata.separator

    @classmethod
    def from_dict(cls, data, separator=None):
        """Instantiate record from a dictionary"""
        return cls(None, data=data, separator=separator)

    def to_dict(self):
        """Export record as dictionary"""
        return self._metadata.to_dict()

    def items(self):
        """Iterate over key, value"""
        return self._metadata.items()

    def pop(self, key):
        """Pop element from data model"""
        return self._metadata.pop(key)

    def keys(self):
        """List keys in data model"""
        return self._metadata.keys()

    def values(self):
        """List value in data model"""
        return self._metadata.values()

    def save_as(self, fp):
        """Save de-id as json"""
        json.dump(self._metadata.to_dict(), fp)

    def get_all_dotty_paths(self):
        """Returns a list of string for all accessible path in record in dotty
        dict notation"""

        def search_in(item):
            dotty_paths = []
            if isinstance(item, list):
                for idx, ita in enumerate(item):
                    dotty_paths.append(idx)
                    search_paths = search_in(ita)
                    dotty_paths += list(
                        map(lambda x, a=idx: f"{a}{self.separator}{x}", search_paths)
                    )
            elif isinstance(item, dict):
                for key, itb in item.items():
                    dotty_paths.append(key)
                    search_paths = search_in(itb)
                    dotty_paths += list(
                        map(lambda x, b=key: f"{b}{self.separator}{x}", search_paths)
                    )
            return dotty_paths

        dotty_paths = []
        for k, item in self._metadata.items():
            dotty_paths.append(k)
            if isinstance(item, list):
                for i, it in enumerate(item):
                    dotty_paths.append(f"{k}{self.separator}{i}")
                    paths = search_in(it)
                    dotty_paths += list(
                        map(
                            lambda x, k=k, i=i: f"{k}{self.separator}{i}{self.separator}{x}",
                            paths,
                        )
                    )
            elif isinstance(item, dict):
                for kk, it in item.items():
                    dotty_paths.append(f"{k}{self.separator}{kk}")
                    paths = search_in(it)
                    dotty_paths += list(
                        map(
                            lambda x, k=k, kk=kk: f"{k}{self.separator}{kk}{self.separator}{x}",
                            paths,
                        )
                    )
        return dotty_paths


class JSONFileProfile(FileProfile):
    """JSON implementation of load/save and remove/replace fields"""

    name = "json"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = []
    record_class = JSONRecord
    default_file_filter = ["*.json", "*.JSON"]
    regex_compatible = True
    date_format = "%Y-%m-%d"  # same as str(date)
    datetime_format = "%Y-%m-%d %H:%M:%S"  # same as str(datetime)
    separator = "."

    def __init__(self, file_filter=None):
        file_filter = file_filter if file_filter else self.default_file_filter
        super(JSONFileProfile, self).__init__(
            packfile_type=self.name, file_filter=file_filter
        )

    def load_config(self, config):
        super(JSONFileProfile, self).load_config(config)
        self.separator = config.get("separator", self.separator)

    def add_field(self, field):
        def deidentify_regex_field(field, profile, state, record):
            """"""
            # Replicate field
            attrs = record.get_all_dotty_paths()
            reg = re.compile(field.fieldname)
            for attr in attrs:
                match = reg.match(attr)
                if match:
                    tmp_field = DeIdField.factory(
                        {"name": attr, field.key: getattr(field, "value", True)}
                    )
                    tmp_field.deidentify(profile, state, record)

        # Patch field.deidentify if fieldname is regexp
        if getattr(field, "_is_regex", None):
            field.deidentify = types.MethodType(deidentify_regex_field, field)

        super(JSONFileProfile, self).add_field(field)

    def load_record(self, state, src_fs, path):
        modified = False
        try:
            with src_fs.open(path, "r") as f:
                record = self.record_class(f, separator=self.separator)
        except Exception:  # pylint: disable=broad-except
            log.warning("IGNORING %s - it is not a %s file!", path, self.name)
            return None, False

        return record, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "w") as f:
            record.save_as(f)

    def read_field(self, state, record, fieldname):
        """Read field from record"""
        try:
            return record[fieldname]
        except (KeyError, AttributeError):
            return None

    def remove_field(self, state, record, fieldname):
        try:
            del record[fieldname]
        except KeyError:
            pass

    def replace_field(self, state, record, fieldname, value):
        record[fieldname] = value
