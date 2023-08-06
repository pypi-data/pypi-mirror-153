"""
Burin Memory Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import MemoryHandler

# Burin imports
from .._log_levels import _check_level
from .buffering_handler import BurinBufferingHandler


class BurinMemoryHandler(BurinBufferingHandler, MemoryHandler):
    """
    A handler which buffers log records in memory.

    This is derived from :class:`BurinBufferingHandler`.

    .. note::

        This is a subclass of :class:`logging.handlers.MemoryHandler` and
        functions identically to it in normal use cases.

    This handler will flush when the buffer reaches the specified *capacity* or
    when a record of the specified *flushLevel* or above is emitted.
    """

    def __init__(self, capacity, flushLevel="ERROR", target=None,
                 flushOnClose=True):
        """
        The *target* handler will be called when this flushes its buffer.

        :param capacity: The number of log records to hold in the buffer before
                         flushing.
        :type capacity: int
        :param flushLevel: If a log record of this level is put in the buffer
                           it will immediately flush the whole buffer.
                           (Default = 'ERROR')
        :type flushLevel: int | str
        :param target: The handler which is called with the log records when
                       the buffer is flushed.
        :type target: BurinHandler
        :param flushOnClose: Whether the buffer should be flushed when the
                             handler is closed.  (Default = **True**)
        :type flushOnClose: bool
        """

        BurinBufferingHandler.__init__(self, capacity)
        self.flushLevel = _check_level(flushLevel)
        self.target = target
        self.flushOnClose = flushOnClose

    # Alias methods from the standard library handler
    set_target = MemoryHandler.setTarget
    should_flush = MemoryHandler.shouldFlush

    def close(self):
        """
        Closes the handler.

        This will also flush the buffer if *flushOnClose* was **True** when the
        handler was initialized.
        """

        try:
            if self.flushOnClose:
                self.flush()
        finally:
            with self.lock:
                self.target = None
                BurinBufferingHandler.close(self)
