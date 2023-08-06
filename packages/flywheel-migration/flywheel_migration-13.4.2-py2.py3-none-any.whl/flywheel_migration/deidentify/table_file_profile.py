"""File profiles for de-identifying table-like file such as e.g. csv, tsv"""
import logging
import types

import pandas as pd

from flywheel_migration.deidentify.file_profile import FileProfile
from flywheel_migration.deidentify.deid_field import DeIdField


log = logging.getLogger(__name__)


class TableRecord:
    """A record to deal with tabular data"""

    def __init__(self, fp, reader=None):
        if hasattr(pd, f"read_{reader}"):
            self.read_method = getattr(pd, f"read_{reader}")
        else:
            raise ValueError(f"Unknown read method for reader: {reader}")
        self.df = self.read_method(fp)  # pylint: disable=invalid-name
        self.save_method = f"to_{self.read_method}"

    def __setitem__(self, key, value):
        # e.g. to set filename attributes on record
        setattr(self, key, value)

    def __getitem__(self, key):
        # e.g. to get filename attributes on record
        return getattr(self, key)

    def __delitem__(self, key):
        if key in self.df.columns:
            self.df.drop(labels=[key], axis=1, inplace=True)
        else:
            delattr(self, key)

    def __len__(self):
        return len(self.df)

    def save_as(self, fp, to=None):
        """Save record to file buffer"""
        if to:
            if hasattr(self.df, f"to_{to}"):
                self.save_method = f"to_{to}"
            else:
                raise ValueError(f"Unknown save method for {to}")
        save_method = getattr(self.df, self.save_method)
        save_method(fp, index=False)

    @property
    def columns(self):
        """Return column of the dataframe"""
        return self.df.columns


class TableFileProfile(FileProfile):
    """FileProfile subclass for tables (e.g. csv, tsv) for de-id COLUMNS"""

    name = "table"
    record_class = TableRecord

    reader = None
    delimiter = None  # character for row, column separation in field definition
    default_file_filter = None
    hash_digits = 16

    def __init__(self, file_filter=None):
        file_filter = file_filter if file_filter else self.default_file_filter
        super(TableFileProfile, self).__init__(
            packfile_type=self.name, file_filter=file_filter
        )

    def load_config(self, config):
        super(TableFileProfile, self).load_config(config)
        self.reader = config.get("reader", self.reader)
        self.delimiter = config.get("delimiter", self.delimiter)

    def to_config(self):
        results = super(TableFileProfile, self).to_config()
        if self.reader != self.__class__.reader:
            results["reader"] = self.reader
        if self.delimiter != self.__class__.delimiter:
            results["delimiter"] = self.delimiter
        return results

    def add_field(self, field):
        def deidentify_by_series(field, profile, state, record):
            """De-identify dataframe series wise"""
            tmp_field = DeIdField.factory(field.to_config())
            for idx, series in record.df.iterrows():
                tmp_field.deidentify(profile, state, series)
                record.df.loc[idx] = series

        # remove action, remove the column and we don't want to patch filename
        # fields
        if field.key != "remove" and not field.fieldname.startswith(
            self.filename_field_prefix
        ):
            field.deidentify = types.MethodType(deidentify_by_series, field)

        super(TableFileProfile, self).add_field(field)

    def load_record(self, state, src_fs, path):
        try:
            with src_fs.open(path, "r") as fp:
                record = self.record_class(fp, reader=self.reader)
        except Exception:  # pylint: disable=broad-except
            log.warning(
                "IGNORING %s - cannot read file with specify reader %s!",
                path,
                self.reader,
            )
            return None, False
        return record, False

    def save_record(self, state, record, dst_fs, path):
        with dst_fs.open(path, "w") as fp:
            record.save_as(fp, to=self.reader)

    def read_field(self, state, record, fieldname):
        # NB: record can also be a series of the dataframe
        try:
            value = record[fieldname]
        except KeyError:
            value = None
        return value

    def remove_field(self, state, record, fieldname):
        try:
            del record[fieldname]
        except KeyError:
            pass

    def replace_field(self, state, record, fieldname, value):
        # NB: record can also be a series of the dataframe
        record[fieldname] = value

    def validate(self, enhanced=False):
        errors = super(TableFileProfile, self).validate(enhanced=enhanced)
        if not self.reader:
            errors.append("Table profile invalid: reader is not defined.")
        else:
            if not hasattr(pd, f"read_{self.reader}"):
                errors.append(f"Unknown read method for reader: {self.reader}")
        return errors


class CSVFileProfile(TableFileProfile):
    """FileProfile class for CSV files"""

    name = "csv"
    delimiter = ","
    reader = "csv"
    default_file_filter = [".csv", ".CSV"]


class TSVFileProfile(TableFileProfile):
    """FileProfile class for TSV files"""

    name = "tsv"
    delimiter = "\t"
    reader = "csv"
    default_file_filter = [".tsv", ".TSV"]
