"""
Burin HTTP Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import HTTPHandler

# Burin imports
from .handler import BurinHandler


allowedMethods = ["GET", "POST"]


class BurinHTTPHandler(BurinHandler, HTTPHandler):
    """
    A handler that can send log records over HTTP to a Web server.

    .. note::

        This is a subclass of :class:`logging.HTTPHandler` and
        functions identically to it in normal use cases.

    .. note::

        This has the :meth:`BurinHTTPHandler.get_connection` method (also
        aliased as :meth:`BurinHTTPHandler.getConnection`); this was added to
        the standard library in Python 3.9 but is available here for all Python
        versions supported by Burin.
    """

    def __init__(self, host, url, method="GET", secure=False, credentials=None,
                 context=None):
        """
        This will setup the handler and do some basic checks of parameters.

        Only 'GET' or 'POST' are allowed as *method*.  Also *context* must be
        **None** if *secure* is **False**.

        :param host: The host to connect to; this can be in the form of
                     'host:port' if non-standard HTTP/HTTPS ports are to be
                     used.
        :type host: str
        :param url: The URL path on the host to use.
        :type url: str
        :param method: The HTTP method to use for the request.  This must be
                       either 'GET' or 'POST'.  (Default = 'GET')
        :type method: str
        :param secure: Whether to use HTTPS or not.  (Default = **False**)
        :type secure: bool
        :param credentials: If authentication is needed for the host then this
                            should be a 2-tuple of (username, password).  This
                            will be placed into an HTTP 'Authorization' header
                            for Basic Authentication support.  If this is used
                            you should also use *secure*=**True** so that the
                            username and password are not sent in cleartext to
                            the host.
        :type credentials: tuple(str, str)
        :param context: A :class:`ssl.SSLContext` instance to configured
                        settings for an HTTPS connection.  This must be
                        **None** if *secure*=**False**.
        :type context: ssl.SSLContext
        :raises ValueError: If *method* is not 'GET' or 'POST', or *context* is
                            not **None** and *secure*=**False**.
        """

        BurinHandler.__init__(self)

        method = method.upper()
        if method not in allowedMethods:
            raise ValueError(f"method must be one of {', '.join(allowedMethods)}")

        if not secure and context is not None:
            raise ValueError("context parameter cannot be used if secure=False")

        self.context = context
        self.credentials = credentials
        self.host = host
        self.method = method
        self.secure = secure
        self.url = url

    # Alias methods from the standard library handler
    map_log_record = HTTPHandler.mapLogRecord

    # HTTPHandler.getConnection was added in Python 3.9; so for 3.6, 3.7, and
    # 3.8 support it is recreated here (based on 3.10.2)
    def get_connection(self, host, secure):
        """
        Gets the HTTP or HTTPS connection.

        This can be overridden to change how the connection is created; for
        example if a proxy is required.

        :param host: The host to connect to.
        :type host: str
        :param secure: Whether to use HTTPS or not.
        :type secure: bool
        :returns: The connection object.
        :rtype: http.client.HTTPConnection | http.client.HTTPSConnection
        """

        import http.client
        if secure:
            connection = http.client.HTTPSConnection(host, context=self.context)
        else:
            connection = http.client.HTTPConnection(host)

        return connection

    # Aliases for better compatibility to replace standard library logging
    getConnection = get_connection
