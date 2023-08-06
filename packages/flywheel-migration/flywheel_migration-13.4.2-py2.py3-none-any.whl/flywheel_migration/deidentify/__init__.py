"""Provides de-identification and subject mapping functionality"""
import json
import logging
import os

from ruamel.yaml import YAML

from .factory import load_subject_map, create_subject_map
from .deid_profile import DeIdProfile
from .exceptions import ValidationError

from . import (
    file_profile,
    dicom_file_profile,
    json_file_profile,
    key_value_text_file_profile,
    filename_file_profile,
)

try:
    from . import (
        jpg_file_profile,
        tiff_file_profile,
        png_file_profile,
        xml_file_profile,
        table_file_profile,
    )
except ImportError:
    # JPG, PNG, TIFF, Table, XML and derivatives file profiles use C libraries which
    # requires shared libraries. this can be problematic for example in case of
    # building cross platform Flywheel CLI binary
    # make this module optional to allow using migration-toolkit in python
    # packages that don't require these profiles.
    pass

log = logging.getLogger("deidentify")


def load_deid_profile(name, enhanced=False):
    """Helper function to load profile either at path or one of the defaults"""
    if os.path.isfile(name):
        return load_profile(name, enhanced=enhanced)

    # Load default profiles
    profiles = load_default_profiles()
    for profile in profiles:
        if profile.name == name:
            return profile

    raise ValueError("Unknown de-identification profile: {}".format(name))


def load_profile(path, enhanced=False):
    """Load the de-identification profile at path"""
    _, ext = os.path.splitext(path.lower())

    config = None
    try:
        if ext == ".json":
            with open(path, "r") as f:
                config = json.load(f)
        elif ext in [".yml", ".yaml"]:
            with open(path, "r") as f:
                yaml = YAML()
                config = yaml.load(f)
    except ValueError:
        log.exception("Unable to load config at: %s", path)

    if not config:
        raise ValueError("Could not load config at: {}".format(path))

    profile = DeIdProfile()
    profile.load_config(config)

    errors = profile.validate(enhanced=enhanced)
    if errors:
        raise ValidationError(path, errors)

    return profile


def load_default_profiles():
    """Load default de-identification profiles"""
    src_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(src_dir, "deid-profiles.yml")

    results = []

    with open(path, "r") as f:
        yaml = YAML()
        profiles = yaml.load(f)

    for config in profiles:
        profile = DeIdProfile()
        profile.load_config(config)
        results.append(profile)

    return results
