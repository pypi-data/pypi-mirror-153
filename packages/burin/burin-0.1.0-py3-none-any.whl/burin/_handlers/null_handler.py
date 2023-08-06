"""
Burin Null Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Burin imports
from .handler import BurinHandler


class BurinNullHandler(BurinHandler):
    """
    A handler that doesn't do any formatting or output any log records.

    This is essentially meant as a no-op handler to be used when you need a
    handler to be attached to a logger, but don't want any output.
    """

    def create_lock(self):
        """
        Does not actually create a lock; this will set *self.lock* to **None**.
        """

        self.lock = None

    def emit(self, record):
        """
        Does not emit anything.

        :param record: This is not emitted to anything; it is only here so the
                       signature matches other handlers.
        :type record: BurinLogRecord
        """
        pass

    def handle(self, record):
        """
        Does no processing or handling of the record.

        :param record: This is not processed in any way; it is only here so the
                       signature matches other handlers.
        :type record: BurinLogRecord
        """
        pass

    def _at_fork_reinit(self):
        """
        Does not do anything as *self.lock* is **None**.
        """
        pass

    # Aliases for better compatibility to replace standard library logging
    createLock = create_lock
