"""
Burin Percent Style Format

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import re

# Burin imports
from .._exceptions import FormatError


class _BurinPercentStyle:
    """
    Percent % style format processor.

    This handles the actual format processing and validation for
    :class:`BurinFormatter` that use % style formatting.
    """

    asctimeFormat = "%(asctime)s"
    asctimeSearch = "%(asctime)"
    defaultFormat = "%(message)s"
    validationPattern = re.compile(r"%\(\w+\)[#0+ -]*(\*|\d+)?(\.(\*|\d+))?[diouxefgcrsa%]", re.I)

    def __init__(self, fmt, *, defaults=None):
        """
        This sets the format string and defaults.

        :param fmt: The format string to use when formatting a log record.
        :type fmt: str
        :param defaults: A dictionary that provides default values for custom
                         fields.  This is a keyword only argument and cannot
                         be passed as a positional argument.
        :type defaults: dict{str: Any}
        """

        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def format(self, record):
        """
        Tries to format the *record*.

        .. note::

            This differs from the style classes in the standard :mod:`logging`
            library as it will raise a :exc:`FormatError` instead of a
            :exc:`ValueError` if there is a problem when formatting the record.

        :param record: The log record to format
        :type record: BurinLogRecord
        :raises FormatError: If a formatting field is not in the log record.
        """

        try:
            return self._format(record)
        except KeyError as err:
            raise FormatError(f"Formatting field not found in record: {err}")

    def uses_time(self):
        """
        Checks whether the time field is in the format string.

        :returns: Whether the time field is in the format string.
        :rtype: bool
        """

        return self._fmt.find(self.asctimeSearch) >= 0

    def validate(self):
        """
        Validates the format string.

        :raises FormatError: If validation of the format string fails.
        """

        if not self.validationPattern.search(self._fmt):
            raise FormatError(f"Invalid format '{self._fmt}' for "
                              f"'{self.default_format[0]}' style")

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

        return self._fmt % values

    # Aliases for better compatibility to replace standard library logging
    asctime_format = asctimeFormat
    asctime_search = asctimeSearch
    default_format = defaultFormat
    validation_pattern = validationPattern
    usesTime = uses_time
