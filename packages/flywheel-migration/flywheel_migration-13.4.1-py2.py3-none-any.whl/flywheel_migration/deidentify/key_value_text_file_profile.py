"""
File profile for de-identifying text files with lines that contain string
    pattern-delimited key-value pairs
"""

import codecs
import logging
import re
import sys

from collections import OrderedDict

from .file_profile import FileProfile


log = logging.getLogger(__name__)


def encoding_supported(enc):
    """Returns boolean indicating whether encoding string is supported."""

    try:
        codecs.lookup(enc)
    except LookupError:
        return False
    return True


class KeyValueTextFileLine:
    """Represents a parsed line from key-value text file"""

    def __init__(self, line, delimiter):
        self.input_line = line
        self.delimiter_pattern = delimiter
        self.key = None
        self.input_value = None
        self.output_value = None
        self.delimiter_value = None
        self.parse_line()

    def parse_line(self):
        """Parses self.input_line to determine delimiter_value, key, and input_value"""
        line_match = re.compile(self.delimiter_pattern).search(self.input_line)
        if line_match:
            self.delimiter_value = line_match.group(0)
            self.key, self.input_value = re.split(
                self.delimiter_pattern, self.input_line.strip("\n")
            )

        self.output_value = self.input_value

    def set_value(self, value):
        """sets self.output_value to value"""
        if self.input_value is not None:
            self.output_value = value

    def get_output_line(self):
        """get the string representation of line with output_value"""
        if self.output_value != self.input_value and self.input_value is not None:
            output_line = self.input_line.replace(self.input_value, self.output_value)

        else:
            output_line = self.input_line

        return output_line


class KeyValueTextFileRecord:
    """
    Represents a text file where each line is a key-value pair delimited by
        delimiter
    """

    def __init__(self, file_object, delimiter, ignore_bad_lines):

        self.delimiter_pattern = delimiter
        self._line_dict = OrderedDict()
        self.delimiter_value_mode = None
        self.parse_lines(file_object, ignore_bad_lines)

    def __len__(self):
        return len(self._line_dict)

    def __getitem__(self, key):
        if key in self._line_dict.keys():
            return self._line_dict[key].output_value

        return getattr(self, key, None)

    def __setitem__(self, key, value):
        if isinstance(self._line_dict.get(key), KeyValueTextFileLine):
            self._line_dict[key].set_value(value)
        else:
            self.insert_key(key, value)

    def __delitem__(self, key):
        if key in self._line_dict.keys():
            return self._line_dict.pop(key)
        if hasattr(self, key):
            delattr(self, key)
        return None

    def parse_lines(self, file_object, ignore_bad_lines):
        """Parses the lines in file_object into self._line_dict"""
        # Initialize list for computing delimiter value mode
        delimiter_list = list()
        for line_count, line in enumerate(file_object):
            if not re.search(self.delimiter_pattern, line):
                err_str = (
                    f"Delimiter {self.delimiter_pattern} was not found in line"
                    f" {line_count} ({line}). "
                )
                if not ignore_bad_lines:
                    err_str = err_str + (
                        "Please edit your regex to match your file or set "
                        '"ignore-bad-lines" to true'
                    )
                    raise ValueError(err_str)

                err_str = err_str + "Ignoring..."
                key = line_count
                log.warning(err_str)
            else:
                key = re.split(self.delimiter_pattern, line)[0]
            if key not in self._line_dict:
                line_object = KeyValueTextFileLine(line, self.delimiter_pattern)
                self._line_dict[key] = line_object
                delimiter_list.append(line_object.delimiter_value)
            else:
                raise ValueError(f"Cannot have more than one value for {key}")
        # For use in upsert
        self.delimiter_value_mode = max(set(delimiter_list), key=delimiter_list.count)

    def insert_key(self, key, value):
        """
        Prepares a new line object given a key and value and adds it to
            self.line_dict
        """
        # Except if key is already defined.
        if key in self._line_dict.keys():
            raise ValueError(f"Key {key} is already defined. Cannot overwrite.")
        line_string = self.delimiter_value_mode.join([key, value])
        # ensure line ends with a newline character
        if not line_string.endswith("\n"):
            line_string = line_string + "\n"
        line_object = KeyValueTextFileLine(line_string, self.delimiter_pattern)
        # add line_object to the line_dict
        self._line_dict[key] = line_object

    def save_as(self, file_object):
        """save text file"""
        output_lines = [value.get_output_line() for value in self._line_dict.values()]
        file_object.writelines(output_lines)


class KeyValueTextFileProfile(FileProfile):
    """key-value text file implementation of load/save and remove/replace fields"""

    name = "key-value-text-file"
    hash_digits = 16
    default_file_filter = ["*.MHD", "*.mhd"]

    def __init__(self, file_filter=None):
        file_filter = file_filter or self.default_file_filter
        super(KeyValueTextFileProfile, self).__init__(
            packfile_type=self.name, file_filter=file_filter
        )
        self.delimiter = None
        self.encoding = sys.getdefaultencoding()
        self.ignore_bad_lines = False

    def load_config(self, config):
        super(KeyValueTextFileProfile, self).load_config(config)

        self.delimiter = config.get("delimiter")
        self.encoding = config.get("encoding", self.encoding)
        self.ignore_bad_lines = config.get("ignore-bad-lines")
        self.validate()

    def to_config(self):
        result = super(KeyValueTextFileProfile, self).to_config()
        result["delimiter"] = self.delimiter
        result["encoding"] = self.encoding
        result["ignore-bad-lines"] = self.ignore_bad_lines
        return result

    def load_record(self, state, src_fs, path):

        try:
            with src_fs.open(path, encoding=self.encoding) as file_object:
                record = KeyValueTextFileRecord(
                    file_object, self.delimiter, self.ignore_bad_lines
                )
        except Exception:  # pylint: disable=broad-except
            log.error(
                "An exception occured while loading key-value file %s",
                path,
                exc_info=True,
            )
            record = None

        return record, False

    def save_record(self, state, record, dst_fs, path):
        if self.encoding is not None and encoding_supported(self.encoding):
            with dst_fs.open(path, "w", encoding=self.encoding) as file_object:
                record.save_as(file_object)

        else:
            with dst_fs.open(path, "w") as file_object:
                record.save_as(file_object)

    def read_field(self, state, record, fieldname):
        try:
            value = record[fieldname]
        except KeyError:
            value = None
        return value

    def remove_field(self, state, record, fieldname):
        del record[fieldname]

    def replace_field(self, state, record, fieldname, value):
        record[fieldname] = value

    def validate(self, enhanced=False):
        errors = super(KeyValueTextFileProfile, self).validate(enhanced=enhanced)

        if not encoding_supported(self.encoding):
            errors.append(
                f"Encoding {self.encoding} is not valid. Refer to "
                "https://docs.python.org/3.7/library/codecs.html#standard-encodings"
                " for supported encodings"
            )
        re_type = type(re.compile(".*"))
        if not isinstance(self.delimiter, (str, re_type)):
            errors.append(
                f"Delimiter is required to be a string or compiled regex, "
                f"but value {self.delimiter} is type {type(self.delimiter)}."
            )

        return errors
