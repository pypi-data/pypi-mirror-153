"""
Burin Stderr Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import sys

# Burin imports
from .handler import BurinHandler
from .stream_handler import BurinStreamHandler


class _BurinStderrHandler(BurinStreamHandler):
    """
    This is a very basic handler that can only output to :obj:`sys.stderr`.

    It's primary use is as a default last resort handler when one is needed.
    """

    def __init__(self, level="NOTSET"):
        """
        This sets the handler up just like a base handler.

        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level)

    @property
    def stream(self):
        """
        This handler will always use :obj:`sys.stderr` as its stream.

        This cannot be modified.
        """
        return sys.stderr
