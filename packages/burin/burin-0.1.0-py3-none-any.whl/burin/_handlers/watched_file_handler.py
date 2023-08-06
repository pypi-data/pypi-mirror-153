"""
Burin Watched File Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import WatchedFileHandler
import io

# Burin imports
from .file_handler import BurinFileHandler


class BurinWatchedFileHandler(BurinFileHandler, WatchedFileHandler):
    """
    A handler that watches for changes to the file.

    .. note::

        This is a subclass of :class:`logging.handlers.WatchedFileHandler` and
        functions identically to it in normal use cases.

    If the file this is logging to changes it will close and then reopen the
    file.

    This is intended for use on Unix/Linux systems and checks for device or
    inode changes.  Such changes would occur if a program like *logrotate* was
    to rotate the file.

    This should not be used on Windows and is not needed as log files are
    opened with exclusive locks and cannot be moved or renamed when in use.
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False,
                 errors=None):
        """
        This will setup the handler and stat the file.

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

        if "b" not in mode:
            encoding = io.text_encoding(encoding)

        BurinFileHandler.__init__(self, filename, mode=mode, encoding=encoding,
                                  delay=delay, errors=errors)

        self.dev = -1
        self.ino = -1
        self._statstream()

    # Alias methods from the standard library handler
    reopen_if_needed = WatchedFileHandler.reopenIfNeeded

    def emit(self, record):
        """
        Emits the record to the file.

        This will check if the file needs to be reopened before writing to it.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        self.reopen_if_needed()
        BurinFileHandler.emit(self, record)
