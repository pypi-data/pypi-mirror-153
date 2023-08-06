"""
Burin File Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging import FileHandler
import io
import os

# Burin imports
from .._log_levels import get_level_name
from .handler import BurinHandler
from .stream_handler import BurinStreamHandler


class BurinFileHandler(BurinStreamHandler, FileHandler):
    """
    A handler for writing log records to a file.

    This is derived from :class:`BurinStreamHandler`.

    .. note::

        This is a subclass of :class:`logging.FileHandler` and
        functions identically to it in normal use cases.
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False,
                 errors=None):
        """
        This will setup the handler using the absolute file path.

        The file that is opened will grow indefinitely while being logged to.
        If this isn't desired consider using the
        :class:`BurinRotatingFileHandler` or
        :class:`BurinTimedRotatingFileHandler` instead.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param mode: The mode that the file is opened with.  (Default = 'a')
        :type mode: str
        :param encoding: The text encoding to open the file with.
        :type encoding: str
        :param delay: Whether to delay opening the file until the first record
                      is emitted.  (Default = **False**)
        :type delay: bool
        :param errors: Specifies how encoding errors are handled.  See
                       :func:`open` for information on the appropriate values.
        :type errors: str
        """

        # Support Path objects being passed in
        filename = os.fspath(filename)

        # Keep the absolute path
        self.baseFilename = os.path.abspath(filename)

        self.mode = mode
        self.encoding = encoding

        # If the file won't be in binary mode then get the proper text encoding
        if "b" not in mode:
            self.encoding = io.text_encoding(encoding)

        self.errors = errors
        self.delay = delay

        # Keep a local reference to the open function so it can be used during
        # Python finalization
        self._builtin_open = open

        if delay:
            # Don't open the stream but call the constructor to set level,
            # formatter, create lock, etc.
            BurinHandler.__init__(self)
            self.stream = None
        else:
            BurinStreamHandler.__init__(self, self._open())

    def close(self):
        """
        Flushes and closes the file.
        """

        with self.lock:
            try:
                if self.stream:
                    try:
                        self.flush()
                    finally:
                        stream = self.stream
                        self.stream = None

                        if hasattr(stream, "close"):
                            stream.close()
            finally:
                # Python issues 19523 and 42378; this is called unconditionally
                # and this relies on self._closed getting set to True from this
                BurinStreamHandler.close(self)

    def emit(self, record):
        """
        Emits a log record to the file.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        # Open the stream if needed
        if self.stream is None:
            if self.mode != "w" or not self._closed:
                self.stream = self._open()

        if self.stream:
            BurinStreamHandler.emit(self, record)

    def _open(self):
        """
        Opens the file.

        :returns: The opened file object.
        :rtype: io.BytesIO | io.StringIO
        """

        return self._builtin_open(self.baseFilename, self.mode,
                                  encoding=self.encoding, errors=self.errors)

    def __repr__(self):
        level = get_level_name(self.level)
        return f"<{self.__class__.__name__} {self.baseFilename} ({level})>"
