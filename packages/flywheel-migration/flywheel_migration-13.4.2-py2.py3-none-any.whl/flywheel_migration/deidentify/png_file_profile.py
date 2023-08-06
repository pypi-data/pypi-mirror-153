"""File profile for de-identifying files storing Exif metadata such as JPEG
More on Exif at https://en.wikipedia.org/wiki/Exif
"""
import logging

import png
from PIL import Image, UnidentifiedImageError

from .file_profile import FileProfile

PUBLIC_CHUNK_TYPES = [
    "IHDR",
    "PLTE",
    "IDAT",
    "IEND",
    "bKGD",
    "cHRM",
    "dSIG",
    "eXIf",
    "gAMA",
    "hIST",
    "iCCP",
    "iTXt",
    "pHYs",
    "sBIT",
    "sPLT",
    "sRGB",
    "sTER",
    "tEXt",
    "tIME",
    "tRNS",
    "zTXt",
]

log = logging.getLogger(__name__)


class PNGRecord:
    """A record for dealing with png file"""

    mime_type = "image/png"

    def __init__(self, fp, mode="r"):  # rw to allow for saving in place
        self.image = Image.open(fp, mode=mode)
        self.path = fp.name
        self.image.load()
        self._metadata = None
        self.validate()

    @property
    def metadata(self):
        """Load Exif metadata"""
        if self._metadata is None:
            # PNG chunk metadata (see https://en.wikipedia.org/wiki/Portable_Network_Graphics for details)
            # We use pypng instead of Pillow for its more extensive support of chunk blocks
            reader = png.Reader(filename=self.path)
            self._metadata = list(
                reader.chunks()
            )  # NB: The row image is a part of chunk (IDAT)
            reader.file.close()
        return self._metadata

    def validate(self):
        """Validate image against expecting type"""
        if self.image.get_format_mimetype() != self.mime_type:
            raise TypeError(f"File is not of type {self.mime_type}")

    def save_as(self, fp, file_type="PNG"):
        """Save deid image

        Args:
            fp: A file object
            file_type: Image format to save as
        """
        if self._metadata:
            png.write_chunks(fp, self.metadata)
        else:
            self.image.save(fp, format=file_type)


class ChunkStr(str):
    """Subclass of string with a few extra attributes related to PNG chunks"""

    def __new__(cls, value, *_args, **_kwargs):
        return super(ChunkStr, cls).__new__(cls, value)

    def __init__(self, _value, is_pub=False, is_unk=False):
        super(ChunkStr, self).__init__()
        self._is_pub = is_pub
        self._is_unk = is_unk

    @property
    def _is_chunk(self):
        return self._is_pub or self._is_unk


class PNGFileProfile(FileProfile):
    """PNG implementation of load/save and remove/replace fields"""

    name = "png"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = []
    default_output_format = "PNG"
    default_file_filter = ["*.png", "*.PNG"]

    def __init__(self, file_filter=None):
        file_filter = file_filter if file_filter else self.default_file_filter
        super(PNGFileProfile, self).__init__(
            packfile_type="png", file_filter=file_filter
        )
        self.remove_private_chunks = False
        self.output_format = self.default_output_format
        self.public_chunks = PUBLIC_CHUNK_TYPES
        self.lc_kw_dict = {c.lower(): c for c in self.public_chunks}

    def create_file_state(self):
        """Create state object for processing files"""
        return {}

    def to_config(self):
        result = super(PNGFileProfile, self).to_config()
        result["remove-private-chunks"] = self.remove_private_chunks
        return result

    def load_config(self, config):
        super(PNGFileProfile, self).load_config(config)
        self.remove_private_chunks = config.get("remove-private-chunks", False)

    def load_record(self, state, src_fs, path):
        modified = False
        try:
            with src_fs.open(path, "rb") as f:
                record = PNGRecord(f)
        except (TypeError, UnidentifiedImageError):
            log.warning("IGNORING %s - it is not a PNG file!", path)
            return None, False

        # Remove private tags before decoding
        if self.remove_private_chunks:
            # pylint: disable=protected-access
            record._metadata = [
                chunk
                for chunk in record.metadata
                if chunk[0].decode() in self.public_chunks
            ]
            modified = True

        return record, modified

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "wb") as f:
            record.save_as(f, file_type=self.output_format)

    def add_field(self, field):
        """Add field to profile"""
        if field.fieldname.lower() in self.lc_kw_dict:
            field.fieldname = ChunkStr(
                self.lc_kw_dict[field.fieldname.lower()], is_pub=True
            )
        elif field.fieldname.startswith(self.filename_field_prefix):
            field.fieldname = field.fieldname
        else:
            field.fieldname = ChunkStr(field.fieldname, is_unk=True)
        super(PNGFileProfile, self).add_field(field)

    def read_field(self, state, record, fieldname):
        """Read field from record"""
        chunk_tag = getattr(fieldname, "_is_chunk", None)
        if chunk_tag:
            value = []  # multiple chunks can have same chunk type
            for chunk in record.metadata:
                if fieldname.encode() == chunk[0]:
                    value.append(chunk[1])
        else:
            value = getattr(record, fieldname, None)

        return value

    def remove_field(self, state, record, fieldname):
        chunk_tag = getattr(fieldname, "_is_chunk", None)
        if chunk_tag:
            # pylint: disable=protected-access
            record._metadata = [
                chunk for chunk in record.metadata if chunk[0] != fieldname.encode()
            ]
        else:
            if hasattr(record, fieldname):
                delattr(record, fieldname)

    def replace_field(self, state, record, fieldname, value):
        chunk_tag = getattr(fieldname, "_is_chunk", None)
        if chunk_tag:
            raise NotImplementedError(
                "replace-field action for this profile is not yet supported"
            )
        super(PNGFileProfile, self).replace_field(state, record, fieldname, value)

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """
        errors = super(PNGFileProfile, self).validate()

        for field in self.fields:
            if getattr(field.fieldname, "_is_pub", None):
                lc_field = field.fieldname.lower()
                if lc_field not in self.lc_kw_dict:
                    errors.append(
                        f"Chunk type not recognized as a public chunk type: {field.fieldname}"
                    )
            else:
                log.info("%s is a private chunk. Validation skipped.", field.fieldname)

            if field.key in [
                "replace-with",
                "hash",
                "hashuid",
                "increment-datetime",
                "increment-date",
            ]:
                errors.append(
                    f"Action is not currently supported for this profile: {field.key}"
                )

        return errors
