"""
Burin Buffering Formatter

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging import BufferingFormatter

# Burin imports
from .formatter import _defaultFormatter


class BurinBufferingFormatter(BufferingFormatter):
    """
    A formatter that can be used for formatting multiple records in a batch.

    .. note::

        This is a subclass of `logging.BufferingFormatter` and functions
        identically to it in normal use cases.
    """

    def __init__(self, linefmt=None):
        """
        This will set a formatter to use for every record.

        If no formatter is set then a default formatter is used.

        :param linefmt: The formatter to use.  If this is **None** then a
                        default formatter will be used.  (Default = **None**)
        :type linefmt: BurinFormatter
        """

        if linefmt:
            self.linefmt = linefmt
        else:
            linefmt = _defaultFormatter

    # Alias methods from the standard library formatter
    format_header = BufferingFormatter.formatHeader
    format_footer = BufferingFormatter.formatFooter
