"""
Burin Socket Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import SocketHandler
import pickle
import struct

# Burin imports
from .handler import BurinHandler


class BurinSocketHandler(BurinHandler, SocketHandler):
    """
    A handler that writes pickled log records to a network socket.

    .. note::

        This is a subclass of :class:`logging.handlers.SocketHandler` but has
        a change that may be incompatible depending on the receiver's Python
        version.

        The default pickle protocol version used is **4** instead of **1**;
        this can be configured though by the *pickleProtocol* parameter which
        was added.

    The pickled data that is sent is just of the log records attribute
    dictionary (*__dict__*) so it can process the event in any way it needs and
    doesn't require Burin to be installed.

    The :func:`make_log_record` function can be used on the receiving end to
    recreate the log record from the pickled data if desired.
    """

    def __init__(self, host, port, pickleProtocol=4):
        """
        This will set the *host* and *port* for the socket to connect to.

        :param host: The address of the host to communicate with.
        :type host: str
        :param port: The port to communicate on.
        :type port: int
        :param pickleProtocol: The pickle protocol version to use.  (Default =
                               4)
        :type pickleProtocol: int
        """

        BurinHandler.__init__(self)
        self.host = host
        self.port = port
        self.pickleProtocol = pickleProtocol

        if port is None:
            self.address = host
        else:
            self.address = (host, port)

        self.sock = None
        self.closeOnError = False
        self.retryTime = None

        # Retry parameters for backing off
        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

    # Alias methods from the standard library handler
    create_socket = SocketHandler.createSocket
    make_socket = SocketHandler.makeSocket

    def close(self):
        """
        Closes and handler and the socket.
        """

        with self.lock:
            sock = self.sock

            if sock:
                self.sock = None
                sock.close()

            BurinHandler.close(self)

    def handle_error(self, record):
        """
        Handles errors which may occur during an *emit()* call.

        This wile close the socket if *self.closeOnError*=**True**; it then
        calls :meth:`BurinHandler.handle_error` to continue with the error
        handling.

        :param record: The log record that was being processed when the error
                       occurred.
        :type record: BurinLogRecord
        """

        if self.closeOnError and self.sock:
            self.sock.close()
            self.sock = None
        else:
            BurinHandler.handle_error(self, record)

    def make_pickle(self, record):
        """
        Pickles the record in a binary format.

        This prepares the record for transmission across the socket.

        :param record: The log record to pickle.
        :type record: BurinLogRecord
        :returns: The pickled representation of the record.
        :rtype: bytes
        """

        # If there is exception info then get the traceback text into exc_text
        if record.exc_info:
            self.format(record)

        recordDict = dict(record.__dict__)
        recordDict["msg"] = record.get_message()
        recordDict["args"] = None
        recordDict["kwargs"] = None
        recordDict["exc_info"] = None

        # Python issue #25685: delete message as it's redundant with msg
        recordDict.pop("message", None)

        # Get pickled record and the lenth prefix
        recordBytes = pickle.dumps(recordDict, self.pickleProtocol)
        recordLength = struct.pack(">L", len(recordBytes))

        return recordLength + recordBytes

    # Aliases for better compatibility to replace standard library logging
    handleError = handle_error
    makePickle = make_pickle
