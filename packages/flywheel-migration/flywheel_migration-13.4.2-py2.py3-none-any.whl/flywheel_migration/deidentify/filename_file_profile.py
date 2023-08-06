"""File profile for de-identifying any file filenames"""
import logging
import os
import re
import shutil
from .file_profile import FileProfile

log = logging.getLogger(__name__)


class FilenameRecord:
    """A simple record class to support only filename deid"""

    def __init__(self, path):
        self.validate(path)
        self._dirname, self._basename = os.path.split(path)

    @staticmethod
    def validate(path):
        """Validate path"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} is not a file")

    def save_as(self, dst_path):
        """Copy source file to destination path"""
        shutil.copy(os.path.join(self._dirname, self._basename), dst_path)


class FilenameFileProfile(FileProfile):
    """Dicom implementation of load/save and remove/replace fields

    This profile subclass is intended to de-identify filename only. It comes handy
    for working with file where datetime, patient ID or UID are stored in plain text within
    the filename.
    """

    name = "filename"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = []
    default_file_filter = "*"

    def __init__(self):
        super(FilenameFileProfile, self).__init__(
            packfile_type="filename", file_filter=self.default_file_filter
        )

    def create_file_state(self):
        """Create state object for processing files"""
        return {}

    def to_config(self):
        result = super(FilenameFileProfile, self).to_config()
        return result

    def load_record(self, state, src_fs, path):
        modified = False
        record = FilenameRecord(os.path.join(src_fs.root_path, path))
        return record, modified

    def save_record(self, state, record, dst_fs, path):
        record.save_as(os.path.join(dst_fs.root_path, path))

    def read_field(self, state, record, fieldname):
        return getattr(record, fieldname, None)

    def remove_field(self, state, record, fieldname):
        setattr(record, fieldname, None)

    def replace_field(self, state, record, fieldname, value):
        setattr(record, fieldname, value)

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """
        errors = super(FilenameFileProfile, self).validate()

        # check all output groups are defined in input-regex
        for filename in self.filenames:
            group_names = []
            if filename.get("input-regex"):  # check regexp
                try:
                    regex = re.compile(filename.get("input-regex"))
                    group_names = regex.groupindex.keys()
                except re.error:
                    # errors got logged already in superclass method, still needs group_names for following validation
                    continue
                regex = re.compile(r"\{([^}]+)\}")
                out_vars = regex.findall(filename.get("output"))
                for ov in out_vars:
                    if ov not in group_names:
                        errors.append(
                            f"Output group {ov} not found in corresponding input-regex"
                        )

        return errors
