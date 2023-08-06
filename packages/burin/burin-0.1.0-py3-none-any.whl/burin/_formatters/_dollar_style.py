"""
Burin Dollar Style Format

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from string import Template

# Burin imports
from .._exceptions import FormatError
from ._percent_style import _BurinPercentStyle


class _BurinDollarStyle(_BurinPercentStyle):
    """
    Dollar $ style format processor.

    This handles the actual format processing and validation for
    :class:`BurinFormatter` that use $ (:class:`string.Template`) style
    formatting.

    This is a subclass of :class:`_BurinPercentStyle`.
    """

    asctimeFormat = "${asctime}"
    asctimeSearch = "${asctime}"
    defaultFormat = "${message}"

    def __init__(self, *args, **kwargs):
        """
        This sets the template using the format string.

        This will simply call :meth:`super().__init__` with all ``*args`` and
        ``**kwargs`` to initialize the class; then it creates the
        :class:`string.Template` instance using the *self._fmt* which is used
        for formatting later.
        """

        super().__init__(*args, **kwargs)
        self._tpl = Template(self._fmt)

    def uses_time(self):
        """
        Checks whether the time field is in the format string.

        :returns: Whether the time field is in the format string.
        :rtype: bool
        """

        return self._fmt.find("$asctime") >= 0 or self._fmt.find(self.asctimeFormat) >= 0

    def validate(self):
        """
        Validates the format string.

        :raises FormatError: If validation of the format string fails.
        """

        pattern = Template.pattern
        fields = set()

        for match in pattern.finditer(self._fmt):
            matchGroups = match.groupdict()

            if matchGroups["named"]:
                fields.add(matchGroups["named"])
            elif matchGroups["braced"]:
                fields.add(matchGroups["braced"])
            elif match.group(0) == "$":
                raise FormatError("Invalid format: bare '$' not allowed")

        if not fields:
            raise FormatError("Invalid format: no fields")

    def _format(self, record):
        """
        Formats the *record*.

        This uses the *self._tpl* instace and *self._defaults* which are set
        during initialization to format the record into text for output.

        .. note::

            This uses :meth:`string.Template.substitute` which can cause errors
            if fields in the format string are not in the log record.

        :param record: The record to format.
        :type record: BurinLogRecord
        :returns: The formatted text of the record.
        :rtype: str
        :raises KeyError: If fields in the format string are not fields in the
                          log record.
        """

        values = record.__dict__ if self._defaults is None else {**self._defaults, **record.__dict__}

        self._tpl.substitute(values)

    # Aliases for better compatibility to replace standard library logging
    asctime_format = asctimeFormat
    asctime_search = asctimeSearch
    default_format = defaultFormat
    usesTime = uses_time
