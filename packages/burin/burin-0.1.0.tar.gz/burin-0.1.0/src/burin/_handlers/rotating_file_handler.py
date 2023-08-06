"""
Burin Rotating File Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import RotatingFileHandler
import io

# Burin imports
from .base_rotating_handler import BurinBaseRotatingHandler


class BurinRotatingFileHandler(BurinBaseRotatingHandler, RotatingFileHandler):
    """
    A handler that rotates the file when it reaches a certain size.

    This is derived from :class:`BurinBaseRotatingHandler`.

    .. note::

        This is a subclass of :class:`logging.handlers.RotatingFileHandler` and
        functions identically to it in normal use cases.

    The file is rotated once it reaches a specific size.  A limit can also be
    placed on how many rotated files are kept.
    """

    def __init__(self, filename, mode="a", maxBytes=0, backupCount=0,
                 encoding=None, delay=False, errors=None):
        """
        This will initialize the handler to write to the file.

        The file will be rotated when it reaches *maxBytes* size.  The number
        of rotated files to keep is set by *backupCount*.

        When the files are rotated a number is appended to the filename in the
        order '.1', '.2', '.3', etc. until the *backupCount* is reached.  So a
        *backupCount* of 5 will result in 5 files other than the active log
        file being kept up to '*filename*.5'.  Once *backupCount* is reached
        the next time a rotate happens the oldest file will be removed.

        The active log file set with *filename* is always the file being
        written to.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param mode: The mode that the file is opened with.  This should be 'a'
                     in almost all use cases.  If 'w' is in the mode and
                     *maxBytes* != 0 then it will be replaced with 'a' as
                     otherwise the file will be truncated every time the
                     program runs which is counter-intuitive to a rotating log
                     file. (Default = 'a')
        :type mode: str
        :param maxBytes: The maximum size (in bytes) the file can be before a
                         rotation happens.  The rotation happens before an emit
                         so the file should never go above this size.  If this
                         is 0 then the file will never be rotated.  (Default =
                         0)
        :type maxBytes: int
        :param backupCount: How many rotated log files to keep.  If this is 0
                            then the file will not be rotated.  (Default = 0)
        :type backupCount: int
        :param encoding: The text encoding to open the file with.
        :type encoding: str
        :param delay: Whether to delay opening the file until the first record
                      is emitted.  (Default = **False**)
        :type delay: bool
        :param errors: Specifies how encoding errors are handled.  See
                       :func:`open` for information on the appropriate values.
        :type errors: str
        """

        # If rotation is desired then it doesn't make sense to use a "w" mode
        # as it would truncate logs from any previous runs
        if maxBytes > 0 and "w" in mode:
            mode = mode.replace("w", "a")

        if "b" not in mode:
            encoding = io.text_encoding(encoding)

        BurinBaseRotatingHandler.__init__(self, filename, mode, encoding=encoding,
                                          delay=delay, errors=errors)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    # Alias methods from the standard library handler
    do_rollover = RotatingFileHandler.doRollover
    should_rollover = RotatingFileHandler.shouldRollover
