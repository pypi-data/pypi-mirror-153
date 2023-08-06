"""File profile for de-identifying TIFF files"""
import os
import logging

from PIL import Image, UnidentifiedImageError
from PIL.TiffTags import TAGS_V2

from .file_profile import FileProfile

log = logging.getLogger(__name__)


class TIFFRecord:
    """A record for dealing with jpg file"""

    mime_type = "image/tiff"
    file_type = "TIFF"

    def __init__(self, fp, mode="r"):  # rw to allow for saving in place
        self.image = Image.open(fp, mode=mode)
        self.image.load()
        self.path = fp.name
        self._metadata = None
        self.validate()

    @property
    def metadata(self):
        """Load metadata"""
        if self._metadata is None:
            self._metadata = self.image.tag_v2
        return self._metadata

    def validate(self):
        """Validate image against expecting type"""
        if self.image.get_format_mimetype() != self.mime_type:
            raise TypeError(f"File is not of type {self.mime_type}")
        if self.image.n_frames > 1:
            raise ValueError(
                f"{self.image.n_frames} frames found in {self.path}. "
                f"Currently only supporting 1 frames"
            )

    def save_as(self, filepath, file_type=None, **kwargs):
        """Save deid image

        Args:
            filepath: A file path
            file_type: Image format to save as
        """
        if not file_type:
            file_type = self.file_type

        try:
            self.image.save(
                filepath, format=file_type, tiffinfo=self.metadata, **kwargs
            )
        except RuntimeError:
            self.image.save(
                filepath, format=file_type, tiffinfo=self.metadata, **kwargs
            )


class IFDTagStr(str):
    """Subclass of string with a few extra attributes related to metadata"""

    def __new__(cls, value, *_args, **_kwargs):
        return super(IFDTagStr, cls).__new__(cls, value)

    def __init__(self, _value, is_ifd=None, idx=None):
        super(IFDTagStr, self).__init__()
        self._is_ifd = is_ifd
        self._idx = idx


class TIFFFileProfile(FileProfile):
    """TIFF implementation of load/save and remove/replace fields

    Human readable tags are leveraged from PIL.TiffTags.TAGS_V2
    """

    name = "tiff"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = []
    datetime_format = "%Y:%m:%d %H:%M:%S"  # YYYY:MM:DD HH:MM:SS
    record_class = TIFFRecord
    private_tags_lower_bound = 32768
    default_output_format = "TIFF"
    default_file_filter = ["*.tif", "*.tiff", "*.TIF", "*.TIFF"]

    def __init__(self, file_filter=None):
        file_filter = file_filter if file_filter else self.default_file_filter
        super(TIFFFileProfile, self).__init__(
            packfile_type=self.name, file_filter=file_filter
        )
        self.remove_private_tags = False
        self.output_format = self.default_output_format
        self.lc_kw_dict = self._build_tags_dict()

    @staticmethod
    def _build_tags_dict():
        # set of all lower-cased  keywords, for later validate()
        lc_kw_dict = {}
        for k, v in TAGS_V2.items():
            lc_kw_dict[v.name.lower()] = {"name": v.name, "idx": k}
        return lc_kw_dict

    def create_file_state(self):
        """Create state object for processing files"""
        return {}

    def to_config(self):
        result = super(TIFFFileProfile, self).to_config()
        result["remove-private-tags"] = self.remove_private_tags
        return result

    def load_config(self, config):
        super(TIFFFileProfile, self).load_config(config)
        self.remove_private_tags = config.get("remove-private-tags", False)

    def load_record(self, state, src_fs, path):
        modified = False
        try:
            with src_fs.open(path, "rb") as f:
                record = self.record_class(f)
        except (TypeError, UnidentifiedImageError):
            log.warning("IGNORING %s - it is not a %s file!", path, self.name)
            return None, False

        # Remove private tags
        if self.remove_private_tags:
            # private tags are stored in the range 32,768 and higher
            for k, _ in record.metadata.items():
                if k >= self.private_tags_lower_bound:
                    del record.metadata[k]
            modified = True

        return record, modified

    def save_record(self, state, record, dst_fs, path):
        record.save_as(
            os.path.join(dst_fs.root_path, path), file_type=self.output_format
        )

    def add_field(self, field):
        """Add field to profile"""
        if field.fieldname.lower() in self.lc_kw_dict:
            ff_lc = self.lc_kw_dict[field.fieldname.lower()]
            field.fieldname = IFDTagStr(ff_lc["name"], idx=ff_lc["idx"], is_ifd=True)
            super(TIFFFileProfile, self).add_field(field)
        else:
            super(TIFFFileProfile, self).add_field(field)

    def read_field(self, state, record, fieldname):
        """Read field from record"""
        ifd_tag = getattr(fieldname, "_is_ifd", None)
        if ifd_tag:
            idx = getattr(fieldname, "_idx", None)
            try:
                value = record.metadata[idx]
            except KeyError:
                value = None
        else:
            value = getattr(record, fieldname, None)

        return value

    def remove_field(self, state, record, fieldname):
        ifd_tag = getattr(fieldname, "_is_ifd", None)
        if ifd_tag:
            idx = getattr(fieldname, "_idx", None)
            try:
                del record.metadata[idx]
            except KeyError:
                pass
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def replace_field(self, state, record, fieldname, value):
        ifd_tag = getattr(fieldname, "_is_ifd", None)
        if ifd_tag:
            idx = getattr(fieldname, "_idx", None)
            try:
                record.metadata[idx] = value
            except KeyError:
                log.info("IFD tag %s (%s) not found, skipping", idx, fieldname)
        else:
            setattr(record, fieldname, value)

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """
        errors = super(TIFFFileProfile, self).validate()

        for field in self.fields:
            lc_field = field.fieldname.lower()
            if lc_field not in self.lc_kw_dict:
                errors.append(f"Not in IFD keyword list: {field.fieldname}")

        return errors
