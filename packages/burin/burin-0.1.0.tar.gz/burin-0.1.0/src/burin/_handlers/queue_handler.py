"""
Burin Queue Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import QueueHandler

# Burin imports
from .handler import BurinHandler


class BurinQueueHandler(BurinHandler, QueueHandler):
    """
    A handler that supports logging messages to a queue.

    .. note::

        This is a subclass of :class:`logging.handlers.QueueHandler` and
        functions identically to it in normal use cases.

    This can be used along with :class:`BurinQueueListener` to allow one
    process or thread in a program handle logging output which may consist of
    slow operations like file writing or sending emails.  This can be useful in
    Web or service applications where responsiveness is important in worker
    processes and threads.

    Logs records are added to the queue by each :class:`BurinQueueHandler` and
    then processed and output by the :class:`BurinQueueListener`.
    """

    def __init__(self, queue):
        """
        This will initialize the handler and set the queue to use.

        :param queue: This must be any queue like object; it does not need to
                      support the task tracking API.
        :type queue: queue.Queue | queue.SimpleQueue | multiprocessing.Queue
        """

        BurinHandler.__init__(self)
        self.queue = queue
