"""File profile for de-identifying files storing Exif metadata such as JPEG
More on Exif at https://en.wikipedia.org/wiki/Exif
"""
import copy
import logging

from PIL import Image, UnidentifiedImageError
import piexif

from .file_profile import FileProfile

log = logging.getLogger(__name__)


class JPGRecord:
    """A record for dealing with jpg file"""

    mime_type = "image/jpeg"
    file_type = "JPEG"

    def __init__(self, fp, mode="r"):  # rw to allow for saving in place
        self.image = Image.open(fp, mode=mode)
        self.image.load()
        self._metadata = None
        self.validate()

    @property
    def metadata(self):
        """Load Exif metadata"""
        if self._metadata is None:
            # Exif metadata (see https://www.media.mit.edu/pia/Research/deepview/exif.html for details)
            self._metadata = (
                piexif.load(self.image.info["exif"])
                if "exif" in self.image.info
                else {}
            )
        return self._metadata

    def validate(self):
        """Validate image against expecting type"""
        if self.image.get_format_mimetype() != self.mime_type:
            raise TypeError(f"File is not of type {self.mime_type}")

    def save_as(self, fp, file_type=None):
        """Save deid image

        Args:
            fp: A file object
            file_type: Image format to save as
        """
        file_type = file_type if file_type else self.file_type
        if self.metadata:
            exif_bytes = piexif.dump(self.metadata)
            self.image.save(fp, exif=exif_bytes, format=file_type)
        else:
            self.image.save(fp, format=file_type)


class ExifTagStr(str):
    """Subclass of string with a few extra attributes related to exif"""

    def __new__(cls, value, *_args, **_kwargs):
        return super(ExifTagStr, cls).__new__(cls, value)

    def __init__(self, _value, is_exif=False, ifd=None, idx=None, original=None):
        super(ExifTagStr, self).__init__()
        self._is_exif = is_exif
        self._ifd = ifd
        self._idx = idx
        self._original = original


class JPGFileProfile(FileProfile):
    """Exif implementation of load/save and remove/replace fields

    Human readable tags are leveraged from `piexif.TAGS`
    """

    name = "jpg"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = []
    datetime_format = "%Y:%m:%d %H:%M:%S"  # YYYY:MM:DD HH:MM:SS
    record_class = JPGRecord
    default_output_format = "JPEG"
    default_file_filter = ["*.jpg", "*.jpeg", "*.JPG", "*.JPEG"]

    def __init__(self, file_filter=None):
        file_filter = file_filter if file_filter else self.default_file_filter
        super(JPGFileProfile, self).__init__(
            packfile_type="jpg", file_filter=file_filter
        )
        self.remove_exif = False
        self.remove_gps = True
        self.output_format = self.default_output_format
        self.lc_kw_dict = self._build_tags_dict()

    @staticmethod
    def _build_tags_dict():
        # set of all lower-cased exif keywords, for later validate() and store "path" to them
        lc_kw_dict = {}
        for k, v in piexif.TAGS.items():
            if k in ["0th", "1st", "Exif", "GPS", "Interop"]:  # only filtering on those
                for kk, vv in v.items():
                    lc_vv = vv["name"].lower()
                    element = {
                        "ifd": k,
                        "idx": kk,
                        "original": vv["name"],
                        "fieldname": f'{k}_{vv["name"]}',
                    }
                    if lc_vv in lc_kw_dict:
                        lc_kw_dict[lc_vv].append(element)
                    else:
                        lc_kw_dict[lc_vv] = [element]
        return lc_kw_dict

    def create_file_state(self):
        """Create state object for processing files"""
        return {}

    def to_config(self):
        result = super(JPGFileProfile, self).to_config()
        result["remove-exif"] = self.remove_exif
        result["remove-gps"] = self.remove_gps
        return result

    def load_config(self, config):
        super(JPGFileProfile, self).load_config(config)
        self.remove_exif = config.get("remove-exif", False)
        self.remove_gps = config.get("remove-gps", False)

    def load_record(self, state, src_fs, path):
        modified = False
        try:
            with src_fs.open(path, "rb") as f:
                record = self.record_class(f)
        except (TypeError, UnidentifiedImageError):
            log.warning("IGNORING %s - it is not a JPEG file!", path)
            return None, False

        # Remove private tags before decoding
        if self.remove_exif:
            record._metadata = {}  # pylint: disable=protected-access
            modified = True

        if self.remove_gps:
            if "GPS" in record.metadata:
                record._metadata["GPS"] = {}  # pylint: disable=protected-access
                modified = True

        return record, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "w") as f:
            record.save_as(f, file_type=self.output_format)

    def add_field(self, field):
        """Add field to profile

        Fields matching keyword found in multiple datablock (i.e. Exif, IFD0 and IFD1) get duplicated
        """
        if field.fieldname.lower() in self.lc_kw_dict:
            # Duplicating field to update other occurrence of config keyword in other IFD blocks
            for f in self.lc_kw_dict[field.fieldname.lower()]:
                new_field = copy.deepcopy(field)
                new_field.fieldname = ExifTagStr(
                    f["fieldname"],
                    is_exif=True,
                    ifd=f["ifd"],
                    idx=f["idx"],
                    original=f["original"],
                )
                super(JPGFileProfile, self).add_field(new_field)
        else:
            super(JPGFileProfile, self).add_field(field)

    def read_field(self, state, record, fieldname):
        """Read field from record"""
        # initialize so that if all else fails, we return None
        value = None
        exif_tag = getattr(fieldname, "_is_exif", None)
        if exif_tag:
            ifd, idx = (
                getattr(fieldname, "_ifd", None),
                getattr(fieldname, "_idx", None),
            )
            try:
                value = record.metadata[ifd][idx]
            except KeyError:
                pass

        elif fieldname.lower() in self.lc_kw_dict:
            # Handles case where the fieldname is passed as an element of filename.output without
            # an IFD attached to it (i.e. 0th_, 1st_ or Exif_). Requires lookup in lc_kw_dict.
            # First found get precedence
            for f in self.lc_kw_dict[fieldname.lower()]:
                value = record.metadata[f["ifd"]].get(f["idx"])
                if value:
                    value = value.decode("utf8")
                    break
        else:
            value = getattr(record, fieldname, None)

        # decode value
        if (
            fieldname in self.field_map
        ):  # require for filenames manipulation without any field associated to it
            if (
                self.field_map[fieldname].key
                in ["increment-datetime", "hashuid", "hash"]
                and value
            ):
                try:
                    value = value.decode("utf8")
                except (UnicodeDecodeError, AttributeError):
                    pass

        return value

    def remove_field(self, state, record, fieldname):
        exif_tag = getattr(fieldname, "_is_exif", None)
        if exif_tag:
            ifd, idx = (
                getattr(fieldname, "_ifd", None),
                getattr(fieldname, "_idx", None),
            )
            try:
                _ = record.metadata[ifd].pop(idx)
            except KeyError:
                pass
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def replace_field(self, state, record, fieldname, value):
        exif_tag = getattr(fieldname, "_is_exif", None)
        if exif_tag:
            ifd, idx = (
                getattr(fieldname, "_ifd", None),
                getattr(fieldname, "_idx", None),
            )
            try:
                record.metadata[ifd][idx] = value
            except KeyError:
                log.info("Exif %s not found in %s, skipping", fieldname, ifd)
        else:
            setattr(record, fieldname, value)

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """
        errors = super(JPGFileProfile, self).validate()

        for field in self.fields:
            if getattr(field.fieldname, "_is_exif", None):
                fieldname = getattr(field.fieldname, "_original", "")
            else:
                fieldname = field.fieldname
            lc_field = fieldname.lower()
            if lc_field not in self.lc_kw_dict:
                errors.append(f"Not in Exif keyword list: {fieldname}")

        return errors
