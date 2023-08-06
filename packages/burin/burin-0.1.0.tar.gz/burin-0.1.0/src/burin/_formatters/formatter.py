"""
Burin Formatter

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging import Formatter
import time

# Burin imports
from .._exceptions import FormatError
from ._brace_style import _BurinBraceStyle
from ._dollar_style import _BurinDollarStyle
from ._percent_style import _BurinPercentStyle


# The format style map of classes and default basic formats.
_styles = {
    "%": {
        "class": _BurinPercentStyle,
        "default": "%(levelname)s:%(name)s:%(message)s"
    },
    "{": {
        "class": _BurinBraceStyle,
        "default": "{levelname}:{name}:{message}"
    },
    "$": {
        "class": _BurinDollarStyle,
        "default": "${levelname}:${name}:${message}"
    }
}


class BurinFormatter(Formatter):
    """
    Formatter for converting a log record for output.

    .. note::

        This is a subclass of :class:`logging.Formatter` but has some minor
        changes (such as raising :exc:`FormatError` instead of
        :exc:`ValueError`).

        These changes shouldn't impact normal usage when compared with the
        standard :mod:`logging` library.

    Formatters are responsible for converting a log record into (usually) a
    string which can then be output by a handler.

    Below is the attributes of a log record that could be useful to log.  Any
    of these can be added to the format string in whatever formatting style
    that is selected.

    asctime
        Time the log record was created in a human readable format.

    created
        Time the log record was created as returned by :func:`time.time`

    filename
        Filename from where the logging call was issued.

        .. note::
            This is only the filename part; for the whole path see *pathname*

    funcName
        Name of the function where the logging call was issued.

    levelname
        Text name for the logging level of the record.

    levelno
        Numeric value for logging level of the record.

    lineno
        Line number where the logging call was issued.

    message
        Log message as processed by :meth:`BurinLogRecord.get_message` method.

        This is set on the record when :meth:`BurinFormatter.format` is called.

    module
        Module name where the logging call was issued.

    msecs
        Millisecond portion of the time when the log record was created.

    name
        Name of the logger that was called.

    pathname
        Full pathname of the source file where the logging call was issued.

    process
        Process Id

    processName
        Process name

    relativeCreated
        Time in milliseconds from when the log record was created since the
        Burin package was loaded.

    thread
        Thread Id

    threadName
        Thread name

    .. note::

        Some of the attributes may not have values depending on the Python
        implementation used or the values of :attr:`logMultiprocessing`,
        :attr:`logProcesses`, and :attr:`logThreads`.


    .. note::

        There are other attributes of log records which are part of its
        operation and should not need to be formatted.  It is recommended to
        stick to the list above.
    """

    def __init__(self, fmt=None, datefmt=None, style="%", validate=True, *,
                 defaults=None):
        """
        The formatter will use the format string and specified *style*.

        You can use datefmt to change how the time and date are formatted,
        otherwise the default is an ISO8601-like format.

        If no format string is provided a simple style-dependent default is
        used which just includes the message from the log record.

        .. note::

            In Python 3.8 *validate* was added to the standard
            :class:`logging.Formatter`; it is supported here for all versions
            of Python compatible with Burin (including versions below 3.8).

            In Python 3.10 *defaults* was added to the standard
            :class:`logging.Formatter`; it is supported here for all versions
            of Python compatible with Burin (including versions below 3.10).

        :param fmt: The format string to use when formatting a log record.  If
                    this is **None** then a default style-specific format
                    string will be used that has just the log message.
        :type fmt: str
        :param datefmt: The date/time format to use (as accepted by
                        :func:`time.strftime`).  If this is **None** then a
                        default format similar to the ISO8601 standard is used.
        :type datefmt: str
        :param style: The type of formatting to use for the format string.
                      Possible values are '%' for %-formatting, '{' for
                      :meth:`str.format` formatting, and '$' for
                      :class:`string.Template` formatting.  (Default = '%')
        :type style: str
        :param validate: Whether the format should be validated against the
                         style to protect again misconfiguration.
                         (Default = **True**)
        :type validate: bool
        :param defaults: A dictionary that provides default values for custom
                         fields.  This is a keyword only argument and cannot
                         be passed as a positional argument.
        :type defaults: dict{str: Any}
        :raises FormatError: If there are errors with the *format* or *style*,
                             or if *validate* is **True** and validation fails.
        """

        if style not in _styles:
            raise FormatError("Unknown style; must be one of "
                              f"{', '.join(_styles.keys())}")

        self._style = _styles[style]["class"](fmt, defaults=defaults)

        if validate:
            self._style.validate()

        self._fmt = self._style._fmt
        self.datefmt = datefmt

    # Alias methods from the standard library formatter
    format_exception = Formatter.formatException
    format_message = Formatter.formatMessage
    format_stack = Formatter.formatStack
    uses_time = Formatter.usesTime

    def format(self, record):
        """
        Format the record as text.

        The record's attribute dictionary is used for the string formatting
        operation.

        Before the formatting occurs some other steps are taken such as calling
        :meth:`BurinLogRecord.get_message` to get the complete log message, any
        time formatting that may be needed, and exception formatting if
        necessary.

        :param record: The log record to format.
        :type record: BurinLogRecord
        :returns: The log record formatted to text.
        :rtype: str
        """

        # Process the log message.
        record.message = record.get_message()

        # Get time if needed.
        if self.uses_time():
            record.asctime = self.format_time(record, self.datefmt)

        # Get the record text.
        recordText = self.format_message(record)

        # Format exception info if needed.
        if record.exc_info:
            # Only get the traceback text once.
            if not record.exc_text:
                record.exc_text = self.format_exception(record.exc_info)

        # If there is exception info add it to the record text.
        if record.exc_text:
            if recordText[-1:] != "\n":
                recordText += "\n"

            recordText += record.exc_text

        # Add stack info to record text if it's there.
        if record.stack_info:
            if recordText[-1:] != "\n":
                recordText += "\n"

            recordText += self.format_stack(record.stack_info)

        return recordText

    # Formatter.formatTime was modified in Python 3.9; so for matching
    # functionality in 3.6, 3.7, and 3.8 it is recreated here (based on 3.10.2)
    def format_time(self, record, datefmt=None):
        """
        Gets the creation time of the specified log record as formatted text.

        This should be called by the formatter itself within
        :meth:`BurinFormatter.format`; it is separated here to simplify
        overriding how the time is formatted.

        .. note::

            In Python 3.9 this method was changed on the standard
            :class:`logging.Formatter` so that the class attribute
            *default_msec_format* is optional.  This is supported here for all
            versions of Python compatible with Burin (including versions below
            3.9).

        :param record: The log record to get the time from.
        :type record: BurinLogRecord
        :param datefmt: The date/time format to use (as accepted by
                        :func:`time.strftime`).  If **None** then the *datefmt*
                        passed in during initialization of the
                        :class:`BurinFormatter` instance is used.
        :type datefmt: str
        :returns: The formatted date and time of the log record.
        :rtype: str
        """

        recordTime = self.converter(record.created)

        if datefmt:
            creationTime = time.strftime(datefmt, recordTime)
        else:
            creationTime = time.strftime(self.default_time_format, recordTime)

            if self.default_msec_format:
                creationTime = self.default_msec_format % (creationTime, record.msecs)

        return creationTime

    # Aliases for better compatibility to replace standard library logging
    formatTime = format_time


# The default formatter is used in many places if another formatter isn't
# specified
_defaultFormatter = BurinFormatter()
