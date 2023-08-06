"""
Burin Buffering Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import BufferingHandler

# Burin imports
from .handler import BurinHandler


class BurinBufferingHandler(BurinHandler, BufferingHandler):
    """
    A handler that stores log records in a buffer.

    .. note::

        This is a subclass of :class:`logging.handlers.BufferingHandler` and
        functions identically to it in normal use cases.

    Each time a record is added to the buffer a check is done to see if the
    buffer should be flushed.

    This class is intended to be subclassed by other handlers that need to use
    a buffering pattern and should not be instantiated directly except within a
    subclass *__init__* method.
    """

    def __init__(self, capacity):
        """
        The buffer will flush once *capacity* number of records are stored.

        :param capacity: The number of log records to hold in the buffer before
                         flushing.
        :type capacity: int
        """

        BurinHandler.__init__(self)
        self.capacity = capacity
        self.buffer = []

    # Alias methods from the standard library handler
    should_flush = BufferingHandler.shouldFlush

    def close(self):
        """
        Closes the handler and flush the buffer.
        """

        try:
            self.flush()
        finally:
            BurinHandler.close(self)
