"""
Burin Base Rotating Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import BaseRotatingHandler

# Burin imports
from .file_handler import BurinFileHandler


class BurinBaseRotatingHandler(BurinFileHandler, BaseRotatingHandler):
    """
    Base class for handlers that rotate log files.

    This is derived from :class:`BurinFileHandler`.

    .. note::

        This is a subclass of :class:`logging.handlers.BaseRotatingHandler` and
        functions identically to it in normal use cases.

    This should not be instantiated directly except within a subclass
    *__init__* method.
    """

    namer = None
    rotator = None

    def __init__(self, filename, mode, encoding=None, delay=False, errors=None):
        """
        This will initialize the handler for outputting to a file.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param mode: The mode that the file is opened with.
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

        BurinFileHandler.__init__(self, filename, mode=mode, encoding=encoding,
                                  delay=delay, errors=errors)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors

    def do_rollover(self):
        """
        This method should perform the rotation of the file.

        This should be implemented within a subclass and will only raise a
        :exc:`NotImplementedError` in this base class.

        :raises NotImplementedError: As this is not implemented in the base
                                     class.
        """

        raise NotImplementedError("do_rollover must be implemented by"
                                  "BurinBaseRotatingHandler subclasses")

    def emit(self, record):
        """
        Emits the record to the file.

        This will check if the file should be rotated by calling
        *should_rollover* and if that returns **True** it calls *do_rollover*
        to perform the actual rotation.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            if self.should_rollover(record):
                self.do_rollover()

            BurinFileHandler.emit(self, record)
        except Exception:
            self.handle_error(record)

    def should_rollover(self):
        """
        This method should check if the rotation of the file should be done.

        This should be implemented within a subclass and will only raise a
        :exc:`NotImplementedError` in this base class.

        :raises NotImplementedError: As this is not implemented in the base
                                     class.
        """

        raise NotImplementedError("should_rollover must be implemented by"
                                  "BurinBaseRotatingHandler subclasses")

    # Aliases for better compatibility to replace standard library logging
    doRollover = do_rollover
    shouldRollover = should_rollover
