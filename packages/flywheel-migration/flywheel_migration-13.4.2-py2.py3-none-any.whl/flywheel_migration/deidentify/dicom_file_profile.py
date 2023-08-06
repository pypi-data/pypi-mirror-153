"""File profile for de-identifying dicom files"""
import collections
import datetime
import gzip
import logging
import os
import re
import sys

import pydicom
import pydicom.datadict
import pydicom.tag
from pydicom.filebase import DicomBytesIO
from pydicom.data import get_testdata_files
import six
from fs.osfs import OSFS
from flywheel_metadata.file.dicom.fixer import fw_pydicom_config
from flywheel_metadata.file.dicom import extend_private_dictionaries

from flywheel_migration.util import (
    date_delta,
    is_dicom,
    dict_paths,
    walk_dicom_wild_sequence,
    get_dicom_data_elements_hex_path,
    get_dicom_data_elements_keyword_path,
)
from flywheel_migration.deidentify.file_profile import FileProfile
from flywheel_migration.deidentify.deid_field import DeIdField, DeIdFieldMixin

log = logging.getLogger(__name__)

# extend pydicom dictionaries
extend_private_dictionaries()

# match name of type hex, e.g. 0x00100020 or 00100020
DICOM_TAG_HEX_RE = re.compile(r"^(0x)?[0-9a-fA-F]{8}$")
# match name of type tuple, e.g. (0010, 0020)
DICOM_TAG_TUPLE_RE = re.compile(r"\(\s*([0-9a-fA-F]{4})\s*,\s*([0-9a-fA-F]{4})\s*\)")
# match name of type private, e.g. (GGGG, <PrivateTagCreator>, EE)
# Per standard, PrivateTagCreator cannot contain \. Excluding ,"() as well for notation
DICOM_TAG_PRIVATE_RE = re.compile(
    r"^\(\s*([0-9a-fA-F]{4})\s*,\s*(?:\"?)([^,\\\"\(\)]{1,64})(?:\"?)\s*,\s*([0-9a-fA-F]{2})\s*\)$"
)
# match name of type nested sequence, e.g.
# - OtherPatientIDsSequence.0.PatientID
# - 00101002.0.00100020
# - 00101002.0.PatientID
# - OtherPatientIDsSequence.0.00100020
# - OtherPatientIDsSequence.100.00100020
# - OtherPatientIDsSequence.*.00100020
DICOM_NESTED_RE = re.compile(
    r"^(?:([0-9A-Fa-f]{8}|[\w]+)\.((?:[\d]+)|[*])\.)+([0-9A-Fa-f]{8}|[\w]+)$"
)
# match name of type repeater group, e.g. '(50XX, 0010)'
DICOM_TAG_REPEATER_TUPLE_RE = re.compile(
    r"\(\s*([56]0[Xx]{2})\s*,\s*([0-9a-fA-F]{4})\s*\)"
)
# match name of type repeater group, e.g. '50XX0010'
DICOM_TAG_REPEATER_HEX_RE = re.compile(r"^(?:0x)?([56]0[Xx]{2}[0-9a-fA-F]{4})$")
# match name of type hex including dotty sequence, e.g. '00101002.0.00100020'
DICOM_DOTTY_HEX_RE = re.compile(
    r"^([0-9A-Fa-f]{8})((\.((?:[\d]+)?)\.)+([0-9A-Fa-f]{8}))?$"
)

UID_FIELDS = ["SOPInstanceUID", "SeriesInstanceUID", "StudyInstanceUID"]


class DicomTagStr(str):
    """Subclass of string that host attributes/methods to handle the different means
    field can reference Dicom data element(s)"""

    # list of methods to be used for parsing field name
    parsers_method_prefix = "_parse"

    def __new__(cls, value, *_args, **_kwargs):
        if isinstance(value, int):
            # for human readable representation of hex
            value = str(pydicom.tag.Tag(value))
        return super(DicomTagStr, cls).__new__(cls, value)

    def __init__(self, _value, *args, **kwargs):
        super(DicomTagStr, self).__init__(*args, **kwargs)
        self._is_sequence = False
        self._is_private = False
        self._is_repeater = False
        self._dicom_tag = self.parse_field_name(_value)
        self._is_wild_sequence = None

    @property
    def dicom_tag(self):
        return self._dicom_tag

    @property
    def is_sequence(self):
        return self._is_sequence

    @property
    def is_private(self):
        return self._is_private

    @property
    def is_repeater(self):
        return self._is_repeater

    @property
    def is_wild_sequence(self):
        if self._is_wild_sequence is None:
            if (
                self.dicom_tag
                and self.is_sequence
                and "*" in list(map(str, self.dicom_tag))
            ):
                self._is_wild_sequence = True
            else:
                self._is_wild_sequence = False
        return self._is_wild_sequence

    @property
    def is_flat(self):
        """Return True for 'flat' fieldname (map to a single tag), False otherwise."""
        if self.is_repeater or self.is_wild_sequence:
            return False
        return True

    def _parse_tag_tuple(self, name):
        """Process a field name of type tuple (e.g. (0010, 0020)).

        Args:
            name (str): A field name.

        Returns:
            pydicom.Tag or None: If name matches DICOM_TAG_TUPLE_RE, returns a Tag,
              None otherwise.
        """
        match = DICOM_TAG_TUPLE_RE.match(name)
        if match:
            # converting "GGGG"+"EEEE" to hex int, then Tag.
            return pydicom.tag.Tag(int(match.group(1) + match.group(2), 16))
        return None

    def _parse_tag_hex(self, name):
        """Process a field name of type hex notation (e.g. 0x00100020).

        Args:
            name (str): A field name.

        Returns:
            pydicom.Tag or None: If name matches DICOM_TAG_HEX_RE, returns a Tag,
              None otherwise.
        """
        match = DICOM_TAG_HEX_RE.match(name)
        if match:
            # converting "GGGGEEEE" hex int, then Tag.
            return pydicom.tag.Tag(int(name, 16))
        return None

    def _parse_tag_private(self, name):
        """Process a field name of type private tag with PrivateCreator defined
        (e.g. (0009, "GEMS_IDEN_01", 11)).
        Details at http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_7.8.html

        Args:
            name (str): A field name.

        Returns:
            list or None: If ``name`` matches DICOM_TAG_PRIVATE_RE, returns a list of
            [int(GGGG), PrivateCreatorString, int(EE)], None otherwise.
        """
        match = DICOM_TAG_PRIVATE_RE.match(name)
        if match:
            self._is_private = True
            return [int(match.group(1), 16), match.group(2), int(match.group(3), 16)]
        return None

    def _parse_nested(self, name):
        """Process a field name of type nested sequence (e.g. BlaSequence.0.Keyword
        but can be any arbitrary depth).

        Args:
            name (str): A field name.

        Returns:
            list or None: If ``name`` matches DICOM_NESTED_RE, returns a list of
               [Tag, index, Tag, ...] (odd number of items), None otherwise.
        """
        match = DICOM_NESTED_RE.match(name)
        if match:
            # breaking dotty string in its part (either keyword, hex int or *)
            nested_seq_items = re.findall(r"((?:0x)?[0-9A-Fa-f]{8}|[\w]+|[*])+", name)
            tag_seq = []
            for i, item in enumerate(nested_seq_items):
                if i % 2 == 0:  # even i are either keyword or hex tag
                    if DICOM_TAG_HEX_RE.match(item):
                        tag_seq.append(pydicom.tag.Tag(int(item, 16)))
                    else:
                        try:
                            tag_seq.append(pydicom.tag.Tag(item))
                        except ValueError as exc:
                            log.error(f"{item} is not a valid Dicom keyword")
                            raise exc
                else:  # odd i are expected to be coercible as integer or being '*'
                    if item == "*":
                        tag_seq.append(item)
                    else:
                        tag_seq.append(int(item))
            self._is_sequence = True
            return tag_seq
        return None

    def _parse_repeater_group_name(self, name):
        """Returns standardized representation of repeater groups (e.g. 50XX0010)"""
        match = DICOM_TAG_REPEATER_HEX_RE.match(name)
        if match:
            self._is_repeater = True
            return match.group(1).replace("x", "X")
        match = DICOM_TAG_REPEATER_TUPLE_RE.match(name)
        if match:
            self._is_repeater = True
            return f"{match.group(1)}{match.group(2)}".replace("x", "X")

        return None

    def parse_field_name(self, name):
        """Parse the field name and returns

        Args:
            name (str): The field name.

        Returns:
            (list or Tag): Depending on name.

        Raises:
            ValueError: if name matches multiple fieldname definition types.
        """
        if isinstance(name, int):
            return pydicom.tag.Tag(name)

        name = name.strip()

        # process all parsers to checking for uniqueness of match
        parsers = []
        for attr in dir(self):
            if attr.startswith(self.parsers_method_prefix) and callable(
                getattr(self, attr)
            ):
                parsers.append(getattr(self, attr))
        parsers_res = map(lambda f: f(name), parsers)
        parsers_res = list(filter(None, parsers_res))

        if len(parsers_res) > 1:
            raise ValueError(f"{name} matches multiple fieldname notation")
        elif len(parsers_res) == 1:
            return parsers_res[0]
        else:
            return None


class DicomDeIdFieldMixin(DeIdFieldMixin):
    """Mixin to add functionality to DeIdField for Dicom profile"""

    flavor = "Dicom"
    recurse_sequence = False

    def deidentify(self, profile, state, record):
        """Deidentifies depending on field type"""
        fieldnames = self.list_fieldname(record)
        if len(fieldnames) == 0 or (
            len(fieldnames) == 1 and self.fieldname == fieldnames[0]
        ):
            # fieldnames did not get resolved, stick to initial field
            super(DicomDeIdFieldMixin, self).deidentify(profile, state, record)
        else:
            # create a new field for each the resolved fieldnames
            self._deidentify_fieldnames(profile, state, record, fieldnames)

    def _deidentify_fieldnames(self, profile, state, record, fieldnames):
        """Deidentify record based on resolved fieldnames"""
        for fieldname in fieldnames:
            value = self.to_config()
            pop_key = ["name", "regex"]
            for pk in pop_key:
                value.pop(pk, None)
            # using name key, fieldname has been expanded
            tmp_field = DeIdField.factory(
                {"name": fieldname, **value}, mixin=self.__class__
            )
            super(DicomDeIdFieldMixin, tmp_field).deidentify(profile, state, record)

    def list_fieldname(self, record):
        """Returns a list of fieldnames for record depending on field type"""
        if self.is_regex:
            return self._list_fieldname_regex(record)
        elif self.fieldname.is_wild_sequence:
            return self._list_fieldname_wild_sequence(record)
        elif self.recurse_sequence:
            return self._list_fieldname_recurse_sequence(record)
        elif self.fieldname.is_repeater:
            return self._list_fieldname_repeater(record)
        else:
            return super(DicomDeIdFieldMixin, self).list_fieldname(record)

    def _list_fieldname_repeater(self, record):
        """Returns list of Dicom data element paths matching repeater group"""
        # build regular expression (excluding nested sequences)
        regex = f"^{self.fieldname.dicom_tag.replace('XX', '[0-9A-Fa-f]{2}')}$"
        attrs = get_dicom_data_elements_hex_path(record)
        return self._get_regex_match_in_list(regex, attrs)

    def _list_fieldname_wild_sequence(self, record):
        """Returns list of Dicom data element paths as list of keyword and indices
        defined as nested element with wild card (e.g. keyword1.*.keyword2)"""

        def convert_tag_to_hex(tag):
            """Convert to hexadecimal notation (e.g. 0010020) if BaseTag"""
            if isinstance(tag, pydicom.tag.BaseTag):
                return f"{tag:#010x}"[2:]
            else:
                return str(tag)

        dict_tree = walk_dicom_wild_sequence(record, self.fieldname.dicom_tag)
        dcm_tags = list(dict_paths(dict_tree))
        fieldnames = [
            DicomTagStr(".".join(map(convert_tag_to_hex, tag))) for tag in dcm_tags
        ]
        return fieldnames

    def _list_fieldname_regex(self, record):
        """Returns all dicom record attributes, in dotty-notation, matching regex.

        For example, r".*InstanceUID.*" would return of all dotty-path matching
        .*InstanceUID.* such as StudyInstanceUID and any nested element in Sequences
        such as "SomeSequence.0.ReferencedSOPInstanceUID". Supports keywords or indices
        dotty-notation (e.g. .*00100020.* or .*PatientID.*).
        """
        attrs = get_dicom_data_elements_keyword_path(record)
        attrs += get_dicom_data_elements_hex_path(record)
        return self._get_regex_match_in_list(self.fieldname, attrs)

    @staticmethod
    def _get_regex_match_in_list(regex, string_list):
        filtered_list = []
        reg = re.compile(regex)
        for attr in string_list:
            match = reg.match(attr)
            if match:
                filtered_list.append(DicomTagStr(attr))
        return filtered_list

    def _list_fieldname_recurse_sequence(self, record):
        """Return a list of all dicom path matching field including those in SQ element

        Note: self.fieldname can only be a tag, a keyword or a private tag.
        c.f. profile.validate()
        """
        fieldnames = [self.fieldname]
        if self.is_regex:
            raise ValueError(
                f"regex field {self.fieldname} not compatible with recurse-sequence"
            )
        if self.fieldname.is_sequence:
            raise ValueError(
                f"Field {self.fieldname} not compatible with recurse-sequence"
            )

        if self.fieldname.dicom_tag is None:  # keyword
            attrs = get_dicom_data_elements_keyword_path(record)
            fieldnames += [
                DicomTagStr(a) for a in attrs if a.endswith(f".{self.fieldname}")
            ]
        else:
            if self.fieldname.is_private:
                group, private_creator, el = self.fieldname.dicom_tag
                attributes_path = self._get_private_tag_in_sequences(
                    record, group, el, private_creator
                )
                fieldnames += [DicomTagStr(x) for x in attributes_path]
            elif self.fieldname.is_repeater:
                # regex for repeaters defined in sequence only
                regex = f".*{self.fieldname.dicom_tag.replace('XX', '[0-9A-Fa-f]{2}')}$"
                attrs = get_dicom_data_elements_hex_path(record)
                # Not appending because the self.fieldname contains the XX
                fieldnames = self._get_regex_match_in_list(regex, attrs)
            else:  # tag
                attrs = get_dicom_data_elements_hex_path(record)
                index = f"{self.fieldname.dicom_tag:#010x}"[2:]  # cropping 0x
                # if index in sequence should be prefix with a '.'
                fieldnames += [DicomTagStr(a) for a in attrs if a.endswith(f".{index}")]

        return fieldnames

    def _get_private_tag_in_sequences(self, dataset, group, el, private_creator):
        """Returns a list of dotty paths to matching private data elements in dataset
        recursively looping inside sequences"""
        sequences = [el for el in dataset if el.VR == "SQ"]
        fieldnames = []
        for seq in sequences:
            seq_tag_hex = f"{seq.tag:#010x}"[2:]
            for i, ds in enumerate(seq):
                try:
                    el = ds.get_private_item(group, el, private_creator)
                    el_tag_hex = f"{el.tag:#010x}"[2:]
                    fieldnames.append(f"{seq_tag_hex}.{i}.{el_tag_hex}")
                except KeyError:  # tag is not in dataset, skipping
                    pass
                # diving into the SQ element of the dataset
                res = self._get_private_tag_in_sequences(ds, group, el, private_creator)
                if res:  # adding, appending the seq_parent and sequence element index
                    fieldnames += list(
                        map(
                            lambda x, parent=seq_tag_hex, idx=i: f"{parent}.{idx}.{x}",
                            res,
                        )
                    )
        return fieldnames

    def _jitter(self, profile, state, record, jitter_range, jitter_type):
        """Add constraints related to Dicom VR"""
        original = profile.read_field(state, record, self.fieldname)
        new_value = super(DicomDeIdFieldMixin, self)._jitter(
            profile, state, record, jitter_range, jitter_type
        )

        # handle Dicom VR compatibility
        VR = profile.get_data_element_VR(record, self.fieldname)
        if VR in ["IS", "UL", "US"]:  # integer string
            if not isinstance(new_value, int):
                log.warning(
                    f"Casting {self.fieldname} to integer to match VR={VR}. "
                    f"Consider changing jitter-type for this field."
                )
                new_value = int(new_value)
        if VR in ["UL", "US"]:
            if new_value < 0:
                log.warning(
                    f"Jitter on {self.fieldname} yielded a negative value which is "
                    f"incompatible with data element VR={VR}. 0 will be used as new value."
                )
                new_value = 0
            if VR == "US" and new_value > 65535:
                log.warning(
                    f"Jitter on {self.fieldname} yielded a value too large "
                    f"data element with VR={VR}. 65535 will be used as new value."
                )
                new_value = 65535

        if original is not None and original == new_value:
            log.warning(
                f"Jitter on {self.fieldname} yielded the same value as original. "
                f"Consider adjusting your jitter_range"
            )

        return new_value


class DicomFileProfile(FileProfile):
    """Dicom implementation of load/save and remove/replace fields"""

    name = "dicom"
    hash_digits = 16  # How many digits are supported for 'hash' action
    log_fields = ["StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID"]
    regex_compatible = True
    decode = True  # If set to True, will attempt to decode the record upon loading
    remove_undefined = False  # If set to True, remove attributes not defined in fields
    deidfield_mixin = DicomDeIdFieldMixin
    # If set to True, profile is applied to all SQ data elements recursively
    recurse_sequence = False

    def __init__(self):
        super(DicomFileProfile, self).__init__(packfile_type="dicom")

        self.patient_age_from_birthdate = False
        self.patient_age_units = None

        self.remove_private_tags = False

        # set of all lower-cased DICOM keywords, for later validate()
        self.lc_kw_dict = {
            keyword.lower(): keyword
            for keyword in pydicom.datadict.keyword_dict
            if keyword  # non-blank
        }

    def add_field(self, field):
        # Handle tag conversion for later
        field.fieldname = DicomTagStr(field.fieldname)
        if self.recurse_sequence:
            field.recurse_sequence = True
        super(DicomFileProfile, self).add_field(field)

    def create_file_state(self):
        """Create state object for processing files"""
        return {"series_uid": None, "session_uid": None, "sop_uids": set()}

    def get_dest_path(self, state, record, path):
        """Returns default named based on SOPInstanceUID or one based on profile if
        defined"""
        if not self.filenames:
            # Destination path is sop_uid.modality.dcm
            sop_uid = self.get_value(state, record, "SOPInstanceUID")
            if not sop_uid:
                return path
            modality = self.get_value(state, record, "Modality") or "NA"
            dest_path = "{}.{}.dcm".format(sop_uid, modality.replace("/", "_"))
        else:
            dest_path = super(DicomFileProfile, self).get_dest_path(state, record, path)
        return dest_path

    def to_config(self):
        result = super(DicomFileProfile, self).to_config()

        result["patient-age-from-birthdate"] = self.patient_age_from_birthdate
        if self.patient_age_units:
            result["patient-age-units"] = self.patient_age_units

        result["remove-private-tags"] = self.remove_private_tags

        result["decode"] = self.decode

        result["recurse-sequence"] = self.recurse_sequence

        result["remove-undefined"] = self.remove_undefined

        return result

    def load_config(self, config):
        self.patient_age_from_birthdate = config.get(
            "patient-age-from-birthdate", self.patient_age_from_birthdate
        )
        self.patient_age_units = config.get("patient-age-units", self.patient_age_units)
        self.remove_private_tags = config.get(
            "remove-private-tags", self.remove_private_tags
        )
        self.decode = config.get("decode", self.decode)
        self.remove_undefined = config.get("remove-undefined", self.remove_undefined)
        if self.remove_undefined:
            log.info(
                "remove-undefined is set to True in the de-id profile. \n"
                "   All tags not defined under fields will be removed. This may\n"
                "   may lead to invalid Dicom if your profile is not conforming"
                "   to your Dicom SOP Class requirements."
            )
        self.recurse_sequence = config.get("recurse-sequence", self.recurse_sequence)
        super(DicomFileProfile, self).load_config(config)

    @fw_pydicom_config()
    def load_record(self, state, src_fs, path):  # pylint: disable=too-many-branches
        modified = False
        try:
            with src_fs.open(path, "rb") as f:
                # Extract gzipped dicoms
                _, ext = os.path.splitext(path)
                if ext.lower() == ".gz":
                    f = gzip.GzipFile(fileobj=f)

                # Read and decode the dicom
                dcm = pydicom.dcmread(f, force=True)

                # Remove private tags before decoding
                if self.remove_private_tags:
                    dcm.remove_private_tags()
                    modified = True

                if self.decode:
                    dcm.decode()

                if not dcm.dir():
                    # assuming that a Dicom has at least one known tag
                    raise TypeError("Not a DICOM file")

        except Exception:  # pylint: disable=broad-except
            if not is_dicom(src_fs, path):
                log.warning("IGNORING %s - it is not a DICOM file!", path)
                return None, False
            if self.deid_name != "none":
                log.warning("IGNORING %s - cannot deid an invalid DICOM file!", path)
                return None, False

            log.warning('Packing invalid dicom %s because deid profile is "none"', path)
            return True, False

        # Validate the series/session
        series_uid = dcm.get("SeriesInstanceUID")
        session_uid = dcm.get("StudyInstanceUID")

        if state["series_uid"] is not None:
            # Validate SeriesInstanceUID
            if series_uid != state["series_uid"]:
                log.warning(
                    "DICOM %s has a different SeriesInstanceUID (%s) from the rest of the series: %s",
                    path,
                    series_uid,
                    state["series_uid"],
                )
            # Validate StudyInstanceUID
            elif session_uid != state["session_uid"]:
                log.warning(
                    "DICOM %s has a different StudyInstanceUID (%s) from the rest of the series: %s",
                    path,
                    session_uid,
                    state["session_uid"],
                )
        else:
            state["series_uid"] = series_uid
            state["session_uid"] = session_uid

        # Validate SOPInstanceUID
        sop_uid = dcm.get("SOPInstanceUID")
        if sop_uid:
            if sop_uid in state["sop_uids"]:
                log.error(
                    "DICOM %s re-uses SOPInstanceUID %s, and will be excluded!",
                    path,
                    sop_uid,
                )
                return None, False
            state["sop_uids"].add(sop_uid)

        # Set patient age from date of birth, if specified
        if self.patient_age_from_birthdate:
            dob = dcm.get("PatientBirthDate")
            study_date = dcm.get("StudyDate")

            if dob and study_date:
                try:
                    study_date = datetime.datetime.strptime(
                        study_date, self.date_format
                    )
                    dob = datetime.datetime.strptime(dob, self.date_format)

                    # Max value from dcm.py:84
                    age, units = date_delta(
                        dob,
                        study_date,
                        desired_unit=self.patient_age_units,
                        max_value=960,
                    )
                    dcm.PatientAge = "%03d%s" % (age, units)
                    modified = True
                except ValueError as err:
                    log.debug("Unable to update patient age in file %s: %s", path, err)

        # Remove all fields that are not defined in de-id profile
        if self.remove_undefined:
            self.remove_undefined_fields(state, dcm)

        return dcm, modified

    def remove_undefined_fields(self, state, record):
        """Remove data elements not defined in fields"""
        # building keep_tags, a list of dotty paths in hexadecimal
        # (e.g. ['00101002', '00101002.0.00100020']) corresponding to all data elements
        # referenced in the de-id profile fields section.
        keep_tags = []
        for field in self.fields:
            fieldnames = field.list_fieldname(record)
            for fieldname in fieldnames:
                if DICOM_DOTTY_HEX_RE.match(fieldname):
                    # already in the right format, appending
                    keep_tags.append(str(fieldname))
                elif fieldname.is_sequence:
                    # e.g. dicom_tag as [tag, int, tag, ...].
                    # Formatting in hex dotty path notation
                    hex_path = []
                    for dt in fieldname.dicom_tag:
                        if isinstance(dt, pydicom.tag.BaseTag):
                            # format to hex notation GGGGEEEE
                            hex_path.append(f"{dt:#010x}"[2:])
                        else:  # integer
                            hex_path.append(str(dt))
                    # Adding all parents of that nested data element
                    # e.g. if hex_path = ['00101002', '0', '00100020'], adding ['00101002']
                    for i in range(len(hex_path)):
                        if i % 2 == 0:  # need to join hex_path[: odd_number]
                            keep_tags.append(".".join(hex_path[: i + 1]))
                else:
                    data_element = self.get_data_element(record, fieldname)
                    if data_element:
                        keep_tags.append(f"{data_element.tag:#010x}"[2:])

        all_tags = get_dicom_data_elements_hex_path(record)
        for tag in all_tags:
            if tag not in keep_tags:
                fieldname = DicomTagStr(tag)
                self.remove_field(state, record, fieldname)

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "wb") as f:
            record.save_as(f)

    def get_data_element(self, record, fieldname):
        """Returns data element in record at fieldname"""
        data_element = None
        if isinstance(fieldname, DicomTagStr) and fieldname.dicom_tag:
            if fieldname.is_sequence:
                data_element = self._get_data_element_if_sequence(
                    record, fieldname.dicom_tag
                )
            elif fieldname.is_private:
                try:
                    data_element = self._get_data_element_if_private(
                        record, fieldname.dicom_tag
                    )
                except KeyError:
                    data_element = None
            else:
                if fieldname.dicom_tag.group == 2:  # file_meta group
                    data_element = record.file_meta.get(fieldname.dicom_tag)
                else:
                    data_element = record.get(fieldname.dicom_tag)
        else:
            # keyword
            tag = pydicom.datadict.tag_for_keyword(fieldname)
            if tag and pydicom.tag.Tag(tag).group == 2:
                if fieldname in record.file_meta:
                    data_element = record.file_meta[fieldname]
            else:
                if fieldname in record:
                    data_element = record[fieldname]
        return data_element

    def get_data_element_VR(self, record, fieldname):
        """Returns data element VR in record at fieldname"""
        data_element = self.get_data_element(record, fieldname)
        if data_element:
            return data_element.VR
        return None

    def _get_data_element_if_private(self, record, private_dicom_tag):
        """Returns private dicom data element at private_dicom_tag
        (formatted as [GGGG, PrivateCreator, EE])"""
        return record.get_private_item(
            private_dicom_tag[0], private_dicom_tag[2], private_dicom_tag[1]
        )

    def _get_data_element_if_sequence(self, record, tag):
        """Returns data element at tag (formatted as [tag, int, tag, ...])"""
        if not len(tag) == 1:
            try:
                return self._get_data_element_if_sequence(record[tag[0]], tag[1:])
            except (IndexError, KeyError):
                return None
        return record[tag[0]]

    def _get_or_create_data_element_if_sequence(self, record, tag):
        """Return data element at tag (formatted as [tag, int, tag, ...]),
        creating it if does not exist"""
        if not len(tag) == 1:
            try:
                return self._get_or_create_data_element_if_sequence(
                    record[tag[0]], tag[1:]
                )
            except IndexError:  # extend sequence range
                for _ in range(len(record.value), tag[0] + 1):
                    record.value.append(pydicom.dataset.Dataset())
                return self._get_or_create_data_element_if_sequence(
                    record[tag[0]], tag[1:]
                )
            except KeyError:  # create sequence
                record.add_new(tag[0], pydicom.datadict.dictionary_VR(tag[0]), None)
                return self._get_or_create_data_element_if_sequence(
                    record[tag[0]], tag[1:]
                )
        try:
            return record[tag[0]]
        except KeyError:  # Note: ValueError is raised if tag[0] is not a public tag/keyword
            record.add_new(tag[0], pydicom.datadict.dictionary_VR(tag[0]), None)
            return record[tag[0]]
        except IndexError:  # extend sequence range
            for _ in range(len(record.value), tag[0] + 1):
                record.value.append(pydicom.dataset.Dataset())

    def _remove_data_element_if_sequence(self, record, tag):
        """Remove data element at tag (formatted as [tag, int, tag, ...])"""
        if len(tag) == 1:
            if tag[0] in record:
                del record[tag[0]]
        else:
            try:
                self._remove_data_element_if_sequence(record[tag[0]], tag[1:])
            except (KeyError, ValueError):
                pass

    def read_field(self, state, record, fieldname):
        data_element = self.get_data_element(record, fieldname)
        if data_element:
            value = data_element.value
        else:  # not a data element, could be a filename attribute
            value = getattr(record, fieldname, None)

        if value is not None and not isinstance(value, six.string_types):
            if isinstance(value, collections.Sequence):
                value = ",".join([str(x) for x in value])
            else:  # Unknown value, just convert to string
                value = str(value)
        return value

    def remove_field(self, state, record, fieldname):
        if isinstance(fieldname, DicomTagStr) and fieldname.dicom_tag:
            if fieldname.is_sequence:  # this is a sequence
                self._remove_data_element_if_sequence(record, fieldname.dicom_tag)
            elif fieldname.is_private:
                try:
                    de = self._get_data_element_if_private(record, fieldname.dicom_tag)
                    if de:
                        del record[de.tag]
                except KeyError:
                    pass
            elif fieldname.dicom_tag.group == 2:  # file_meta
                del record.file_meta[fieldname.dicom_tag]
            elif fieldname.dicom_tag in record:
                del record[fieldname.dicom_tag]
        else:
            tag = pydicom.datadict.tag_for_keyword(fieldname)
            if tag and pydicom.tag.Tag(tag).group == 2:
                if hasattr(record.file_meta, fieldname):
                    delattr(record.file_meta, fieldname)
            else:
                if hasattr(record, fieldname):
                    delattr(record, fieldname)

    def replace_field(self, state, record, fieldname, value):
        if isinstance(fieldname, DicomTagStr) and fieldname.dicom_tag:
            if fieldname.is_sequence:  # this is a sequence
                de = self._get_or_create_data_element_if_sequence(
                    record, fieldname.dicom_tag
                )
                de.value = value
            elif fieldname.is_private:
                try:
                    de = self._get_data_element_if_private(record, fieldname.dicom_tag)
                    if de:
                        de.value = value
                except KeyError:
                    # adding private tag in corresponding block if VR can be found
                    try:
                        hex_group = f"{fieldname.dicom_tag[0]:#0{6}x}"
                        # adding 10 to element offset to fit in private_dictionary_VR lookup
                        hex_el = "10" + f"{fieldname.dicom_tag[2]:#0{4}x}"[2:]
                        tag = int(hex_group + hex_el, 16)
                        vr = pydicom.datadict.private_dictionary_VR(
                            tag, fieldname.dicom_tag[1]
                        )
                    except KeyError:  # not found
                        log.error(
                            f"Invalid replace-with action. Unknown VR for tag {fieldname.dicom_tag}."
                        )
                        sys.exit(1)
                    block = record.private_block(
                        fieldname.dicom_tag[0], fieldname.dicom_tag[1], create=True
                    )
                    block.add_new(fieldname.dicom_tag[2], vr, value)
            else:
                try:
                    if fieldname.dicom_tag.group == 2:
                        if fieldname.dicom_tag in record.file_meta:
                            record.file_meta[fieldname.dicom_tag].value = value
                        else:
                            raise KeyError("Tag not in File Meta")
                    else:
                        record[fieldname.dicom_tag].value = value
                except KeyError:
                    # checking public dictionaries to get corresponding VR
                    # if not found, log error and exit until we have a better support
                    # for it.
                    try:
                        vr = pydicom.datadict.dictionary_VR(fieldname.dicom_tag)
                    except KeyError:
                        log.error(
                            f"Invalid replace-with action. Unknown VR for tag {fieldname.dicom_tag}."
                        )
                        sys.exit(1)
                    if fieldname.dicom_tag.group == 2:
                        record.file_meta.add_new(fieldname.dicom_tag, vr, value)
                    else:
                        record.add_new(fieldname.dicom_tag, vr, value)
        else:
            tag = pydicom.datadict.tag_for_keyword(fieldname)
            if tag and pydicom.tag.Tag(tag).group == 2:
                setattr(record.file_meta, fieldname, value)
            else:
                setattr(record, fieldname, value)

    def validate_filenames(self, errors):
        """Validates the filename section of the profile

        Args:
            errors (list): Current list of error message

        Returns:
            (list): Extended list of errors message
        """

        for filename in self.filenames:
            group_names = []
            if filename.get("input-regex"):  # check regexp
                try:
                    regex = re.compile(filename.get("input-regex"))
                    group_names = [x.lower() for x in regex.groupindex.keys()]
                except re.error:
                    # errors got log already in superclass method, still needs group_names for following validation
                    continue

            # check group do not collide with dicom keyword
            lc_kw_list = list(self.lc_kw_dict.keys())
            for grp in group_names:
                if grp in lc_kw_list:
                    errors.append(
                        f"regex group {grp} must be unique. Currently colliding with Dicom keywords"
                    )

            # check output filename keyword are valid
            kws = re.findall(r"\{([^}]+)\}", filename["output"])
            lc_kw_list = list(self.lc_kw_dict.keys()) + group_names
            for kw in kws:
                lc_kw = kw.lower()
                if lc_kw not in lc_kw_list:
                    errors.append(
                        f"Filename output invalid. Group not in Dicom keyword or in regex groups: {kw}"
                    )

        return errors

    @fw_pydicom_config()
    def process_files(self, *args, **kwargs):
        super(DicomFileProfile, self).process_files(*args, **kwargs)

    def _validate_replace_with(self, field, errors):
        """Validate whether value provides to replace-with action is valid for VR"""
        # TODO: extend validation to private tags and none keyword tags
        buffer = DicomBytesIO()
        buffer.is_little_endian = True
        buffer.is_implicit_VR = False
        try:
            vr = pydicom.datadict.dictionary_VR(field.fieldname)
            de = pydicom.DataElement(field.fieldname, vr, field.value)
            pydicom.filewriter.write_data_element(buffer, de)
        except Exception:
            errors.append(
                f"Incorrect value type for Dicom element {field.fieldname} (VR={vr}): {type(field.value).__name__}"
            )

    def _validate_hash(self, field, errors):
        """Validate that VR of data element is string compatible"""
        # TODO: extend validation to private tags and none keyword tags
        vr = pydicom.datadict.dictionary_VR(field.fieldname)
        if (
            vr
            in [
                "AT",
                "FL",
                "FD",
                "OB",
                "OW",
                "OF",
                "SL",
                "SQ",
                "SS",
                "UL",
                "UN",
                "US",
                "OB/OW",
                "OW/OB",
                "OB or OW",
                "OW or OB",
                "UI",
            ]
            or field.fieldname in UID_FIELDS
        ):
            errors.append(
                f"{field.fieldname} cannot be hashed - VR not compatible ({vr})"
            )

    def validate(self, enhanced=False):
        """Validate the profile, returning any errors.

        Args:
            enhanced (bool): If True, test profile execution on a set of test files

        Returns:
            list(str): A list of error messages, or an empty list
        """

        errors = super(DicomFileProfile, self).validate()

        if self.filenames:
            self.validate_filenames(errors)

        for field in self.fields:
            if field.fieldname.startswith(self.filename_field_prefix):
                continue

            # check that no actions on SQ tags is defined with recurse_sequence
            if self.recurse_sequence:
                if field.fieldname.dicom_tag and field.fieldname.is_sequence:
                    errors.append(
                        f"recurse-sequence=True is incompatible with field SQ {field.fieldname}."
                    )
                if field.is_regex:
                    errors.append(
                        f"recurse-sequence=True is incompatible with regex field {field.fieldname}."
                    )

            if field.is_regex:
                # nothing more to check
                continue

            # do not validate if name is a tag or nested
            if (
                DICOM_TAG_HEX_RE.match(field.fieldname)
                or DICOM_TAG_TUPLE_RE.match(field.fieldname)
                or DICOM_NESTED_RE.match(field.fieldname)
            ):
                continue
            if field.fieldname.dicom_tag is None:
                lc_field = field.fieldname.lower()
                if lc_field not in self.lc_kw_dict:
                    errors.append("Not in DICOM keyword list: " + field.fieldname)
                # case difference; correct to proper DICOM spelling
                elif field.fieldname != self.lc_kw_dict[lc_field]:
                    field.fieldname = DicomTagStr(self.lc_kw_dict[lc_field])
            elif field.fieldname.is_private:
                # check group is private and private creator is defined
                # group must be an odd number
                if field.fieldname.dicom_tag[0] % 2 == 0:
                    errors.append("Not a private tag: " + field.fieldname)
                # private creator cannot be empty
                if field.fieldname.dicom_tag[1].strip() == "":
                    errors.append("Private creator is empty for: " + field.fieldname)

            # validate action specifics
            if field.fieldname.lower() in self.lc_kw_dict:
                if field.key == "replace-with":
                    self._validate_replace_with(field, errors)
                if field.key == "hash":
                    self._validate_hash(field, errors)

        if enhanced:
            # Test deid profile on test Dicom files
            test_files = get_testdata_files("*.dcm")
            for test_file in test_files:
                dirname, basename = os.path.split(test_file)
                basename = six.u(basename)  # fs requires unicode
                if basename == "1.3.6.1.4.1.5962.1.1.0.0.0.977067309.6001.0.OT.dcm":
                    continue  # this test file seems to be corrupted
                test_fs = OSFS(dirname)
                try:
                    self.process_files(test_fs, test_fs, [basename])
                except Exception:
                    log.error(
                        "Failed to run profile on pydicom test file %s",
                        basename,
                        exc_info=True,
                    )
                    raise

        return errors
