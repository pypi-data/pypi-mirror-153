"""
Burin Timed Rotating File Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import TimedRotatingFileHandler
from stat import ST_MTIME
import io
import os
import re
import time

# Burin imports
from .base_rotating_handler import BurinBaseRotatingHandler


class BurinTimedRotatingFileHandler(BurinBaseRotatingHandler, TimedRotatingFileHandler):
    """
    A handler that rotates the file at specific intervals.

    This is derived from :class:`BurinBaseRotatingHandler`.

    .. note::

        This is a subclass of
        :class:`logging.handlers.TimedRotatingFileHandler` and functions
        identically to it in normal use cases.

    The file is rotated once at the specified interval.  A limit can also be
    placed on how many rotated files are kept.
    """

    def __init__(self, filename, when="h", interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False, atTime=None,
                 errors=None):
        """
        This will initialize the handler to write to the file.

        The file will be rotated based on the *when*, *interval*, and
        *atTime* values.  The number of rotated files to keep is set by
        *backupCount*.

        +------------+------------------------+----------------------------+
        | *when*     | Interval type          | *atTime* usage             |
        +============+========================+============================+
        | 'S'        | Seconds                | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'M'        | Minutes                | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'H'        | Hours                  | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'D'        | Days                   | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'W0'-'W6'  | | *interval* ignored;  | Time of the day to rotate  |
        |            | | Weekday (0 = Monday) |                            |
        +------------+------------------------+----------------------------+
        | 'MIDNIGHT' | | *interval* ignored;  | Time of the date to rotate |
        |            | | Midnight or *atTime* |                            |
        +------------+------------------------+----------------------------+

        When the files are rotated a time and/or date is appended to the
        filename until the *backupCount* is reached.  The :func:`time.strftime`
        format ``%Y-%m-%d_%H-%M-%S`` is used with later parts stripped off when
        not relevant for the rotation interval selected. Once *backupCount* is
        reached the next time a rotate happens the oldest file will be removed.

        The rotation interval is calculated (during initialization) based on
        the last modification time of the log file, or the current time if the
        file doesn't exist, to determine when the next rotation will occur.

        The active log file set with *filename* is always the file being
        written to.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param when: The type of interval to use when calculating the rotation.
                     Use the table above to see the available options and how
                     they impact the rotation interval.  (Default = 'h')
        :type when: str
        :param interval: The interval to use for the file rotation.  Use the
                         table above to see how this is used in determining the
                         rotation interval.  (Default = 1)
        :type interval: int
        :param backupCount: How many rotated log files to keep.  If this is 0
                            then the file will not be rotated.  (Default = 0)
        :type backupCount: int
        :param encoding: The text encoding to open the file with.
        :type encoding: str
        :param delay: Whether to delay opening the file until the first record
                      is emitted.  (Default = **False**)
        :type delay: bool
        :param utc: Whether to use UTC time or local time.  (Default =
                    **False**)
        :type utc: bool
        :param atTime: The time to use for weekday or 'midnight' (daily at set
                       time) rotations.  Use the table above to see how this is
                       used in determining the rotation interval.
        :type atTime: datetime.time
        :param errors: Specifies how encoding errors are handled.  See
                       :func:`open` for information on the appropriate values.
        :type errors: str
        """

        encoding = io.text_encoding(encoding)
        BurinBaseRotatingHandler.__init__(self, filename, "a", encoding=encoding,
                                          delay=delay, errors=errors)
        self.when = when.upper()
        self.backupCount = backupCount
        self.utc = utc
        self.atTime = atTime

        # Calculate the real rollover interval which is really just a number of
        # calculated seconds.
        if self.when == "S":
            self.interval = 1
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.\w+)?$"
        elif self.when == "M":
            self.interval = 60  # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(\.\w+)?$"
        elif self.when == "H":
            self.interval = 60 * 60  # one hour
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?$"
        elif self.when == "D" or self.when == "MIDNIGHT":
            self.interval = 60 * 60 * 24  # one day
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
        elif self.when.startswith("W"):
            self.interval = 60 * 60 * 24 * 7  # one week
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover "
                                 f"from 0 to 6 (0 is Monday): {self.when}")
            if self.when[1] < "0" or self.when[1] > "6":
                raise ValueError("Invalid day specified for weekly rollover: "
                                 f"{self.when}")
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
        else:
            raise ValueError(f"Invalid rollover interval specified: {self.when}")

        self.extMatch = re.compile(self.extMatch, re.ASCII)
        self.interval *= interval

        # In case a Path object was passed in ensure we have a string for the
        # filename
        filename = self.baseFilename

        if os.path.exists(filename):
            mTime = os.stat(filename)[ST_MTIME]
        else:
            mTime = int(time.time())
        self.rolloverAt = self.compute_rollover(mTime)

    # Alias methods from the standard library handler
    compute_rollover = TimedRotatingFileHandler.computeRollover
    do_rollover = TimedRotatingFileHandler.doRollover
    get_files_to_delete = TimedRotatingFileHandler.getFilesToDelete
    should_rollover = TimedRotatingFileHandler.shouldRollover
