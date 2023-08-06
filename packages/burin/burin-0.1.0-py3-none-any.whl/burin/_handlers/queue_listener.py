"""
Burin Queue Listener

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import QueueListener


class BurinQueueListener(QueueListener):
    """
    Listens for and processes log records queued by :class:`BurinQueueHandler`.

    .. note::

        This is a subclass of :class:`logging.handlers.QueueListener` and
        is just a stub class to provide a matching listener for
        :class:`BurinQueueHandler`.

    This can be used along with :class:`BurinQueueHandler` so that log
    processing and output, which may consist of slow operations like file
    writing or sending emails, can be done outside of worker processes or
    threads where responsiveness may be important.
    """
    pass
