"""
Burin Brace Style Format

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import string
import re

# Burin imports
from .._exceptions import FormatError
from ._percent_style import _BurinPercentStyle


_strFormatter = string.Formatter()


class _BurinBraceStyle(_BurinPercentStyle):
    """
    Brace { style format processor.

    This handles the actual format processing and validation for
    :class:`BurinFormatter` that use { (:meth:`str.format`) style formatting.

    This is a subclass of :class:`_BurinPercentStyle`.
    """

    asctimeFormat = "{asctime}"
    asctimeSearch = "{asctime"
    defaultFormat = "{message}"
    fmtSpec = re.compile(r"^(.?[<>=^])?[+ -]?#?0?(\d+|{\w+})?[,_]?(\.(\d+|{\w+}))?[bcdefgnosx%]?$", re.I)
    fieldSpec = re.compile(r'^(\d+|\w+)(\.\w+|\[[^]]+\])*$')

    def validate(self):
        """
        Validates the format string.

        :raises FormatError: If validation of the format string fails.
        """

        fields = set()

        try:
            # Go through each field in the format string and ensure it matches
            # the correct format for { style formatting.
            for literal, field, spec, conversion in _strFormatter.parse(self._fmt):
                if field:
                    if not self.fieldSpec.match(field):
                        raise FormatError(f"Invalid field name/expression: {field!r}")
                    fields.add(field)

                if conversion and conversion not in "rsa":
                    raise FormatError(f"Invalid conversion: {conversion!r}")

                if spec and not self.fmtSpec.match(spec):
                    raise FormatError(f"Bad specifier: {spec!r}")
        except FormatError as err:
            raise FormatError(f"Invalid format: {err}")

        if not fields:
            raise FormatError("Invalid format: no fields")

    def _format(self, record):
        """
        Formats the *record*.

        This uses the *self._fmt* string and *self._defaults* which are set
        during initialization to format the record into text for output.

        :param record: The record to format.
        :type record: BurinLogRecord
        :returns: The formatted text of the record.
        :rtype: str
        """

        values = record.__dict__ if self._defaults is None else {**self._defaults, **record.__dict__}

        return self._fmt.format(**values)

    # Aliases for better compatibility to replace standard library logging
    asctime_format = asctimeFormat
    asctime_search = asctimeSearch
    default_format = defaultFormat
    field_spec = fieldSpec
    fmt_spec = fmtSpec
