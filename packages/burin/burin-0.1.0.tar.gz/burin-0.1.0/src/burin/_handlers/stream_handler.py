"""
Burin Stream Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging import StreamHandler
import sys

# Burin imports
from .._log_levels import get_level_name
from .handler import BurinHandler


class BurinStreamHandler(BurinHandler, StreamHandler):
    """
    A handler that writes log records to a stream.

    .. note::

        This is a subclass of :class:`logging.StreamHandler` and
        functions identically to it in normal use cases.

    .. note::

        This handler will not close the stream it is writing to as
        :obj:`sys.stdout` and :obj:`sys.stderr` are commonly used.

    .. note::

        This has the :meth:`BurinStreamHandler.set_stream` method (also
        aliased as :meth:`BurinStreamHandler.setStream`); this was added to
        the standard library in Python 3.7 but is available here for all Python
        versions supported by Burin.
    """

    terminator = "\n"

    def __init__(self, stream=None):
        """
        This initializes the handler and sets the *stream* to use.

        If *stream* is **None** then :obj:`sys.stderr` is used by default.

        :param stream: The stream to log to.  If this is **None** then
                       :obj:`sys.stderr` is used.
        :type stream: io.TextIOBase
        """

        BurinHandler.__init__(self)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    # StreamHandler.setStream was added in Python 3.7; so for 3.6 support
    # it is recreated here (based on 3.10.2)
    def set_stream(self, stream):
        """
        Sets the *stream* for the handler to log too.

        If the same *stream* that is *self.stream* is passed in then nothing is
        done.

        When replacing the old stream with a new stream the handler will flush
        itself beforehand.

        :param stream: The stream to set for the handler to use.
        :type stream: io.TextIOBase
        :returns: The old stream that was replaced or **None** if nothing was
                  replaced.
        :rtype: io.TextIOBase | None
        """

        if stream is self.stream:
            oldStream = None
        else:
            oldStream = self.stream

            with self.lock:
                self.flush()
                self.stream = stream

        return oldStream

    def __repr__(self):
        level = get_level_name(self.level)
        name = getattr(self.stream, "name", "")

        # Name could be an int
        name = str(name)
        if name:
            name += " "

        return f"<{self.__class__.__name__} {name}({level})>"

    # Aliases for better compatibility to replace standard library logging
    setStream = set_stream
