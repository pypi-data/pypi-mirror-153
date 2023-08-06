"""
Burin Datagram Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import socket

# Burin imports
from .socket_handler import BurinSocketHandler


class BurinDatagramHandler(BurinSocketHandler):
    """
    A handler that writes log records to a datagram socket.

    The pickled data that is sent is just of the log records attribute
    dictionary (*__dict__*) so it can process the event in any way it needs and
    doesn't require Burin to be installed.

    This is derived from :class:`BurinSocketHandler`.

    .. note::

        The default pickle protocol version used in :class:`BurinSocketHandler`
        is different than what is used in
        :class:`logging.handlers.SocketHandler`.

        Since this is a subclass of the socket handler it is also impacted.

        This should only cause issues if the receiving Python version is much
        older.  However if needed the pickle protocol version used can be
        changed with the *pickleProtocol* parameter.

    The :func:`make_log_record` function can be used on the receiving end to
    recreate the log record from the pickled data if desired.
    """

    def __init__(self, host, port, pickleProtocol=4):
        """
        The *host* and *port* will set address and family of socket used.

        If *port* is specified as **None** then the socket family will be
        :const:`socket.AF_UNIX`; otherwise the socket family is
        :const:`socket.AF_INET`.

        :param host: The address of the host to communicate with.
        :type host: str
        :param port: The port to communicate on.
        :type port: int
        :param pickleProtocol: The pickle protocol version to use.  (Default =
                               4)
        :type pickleProtocol: int
        """

        BurinSocketHandler.__init__(self, host, port, pickleProtocol)
        self.closeOnError = False

    def make_socket(self):
        """
        Makes the UDP (:const:`socket.SOCK_DGRAM`) socket.

        The socket family will be either :const:`socket.AF_UNIX` or
        :const:`socket.AF_INET` depending on the address that was passed in
        during initialization.

        :returns: The UDP socket.
        :rtype: socket.socket
        """

        if self.port is None:
            family = socket.AF_UNIX
        else:
            family = socket.AF_INET

        sock = socket.socket(family, socket.SOCK_DGRAM)
        return sock

    def send(self, msg):
        """
        Sends the pickled log record through the socket.

        This will try to create the socket first if it hasn't been created yet.

        :param msg: The pickled string of the log record.
        :type msg: str
        """

        if self.sock is None:
            self.create_socket()

        self.sock.sendto(msg, self.address)

    # Aliases for better compatibility to replace standard library logging
    makeSocket = make_socket
