"""
Burin SMTP Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import SMTPHandler

# Burin imports
from .handler import BurinHandler


class BurinSMTPHandler(BurinHandler, SMTPHandler):
    """
    A handler that can send emails over SMTP for logging events.

    .. note::

        This is a subclass of :class:`logging.handlers.SMTPHandler` and
        functions identically to it in normal use cases.

    This requires an email server that you have permission to send emails
    through; it cannot be used standalone to send directly to a receiving
    server.
    """

    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None,
                 secure=None, timeout=5.0):
        """
        This will initialize the handler for sending emails.

        The standard SMTP port from :const:`smtplib.SMTP_PORT` is used by
        default; if you need to use a non-standard port then *mailhost* must be
        a tuple in the form of *(host, port)*.

        You can send to multiple recipients by passing a list of addresses to
        *toaddrs*.

        If your SMTP server requires authentication then *credentials* should
        be a list or tuple in the form of *(username, password)*.  If you are
        sending credentials then *secure* should not be **None** to prevent
        them being sent unencrypted.

        :param mailhost: The SMTP server to connect to and send mail through.
                         By default the standard SMTP port is used; if you need
                         to use a custom port this should be a tuple in the
                         form of *(host, port)*.
        :type mailhost: str | tuple(str, int)
        :param fromaddr: The address that the email is sent from.
        :type fromaddr: str
        :param toaddrs: The recipient email addresses.  This can be a single
                        address or a list of multiple addresses.
        :type toaddrs: list[str] | str
        :param subject: The subject line of the email.
        :type subject: str
        :param credentials: If the SMTP server requires authentication you can
                            pass a tuple here in the form
                            *(username, password)*.
        :type credentials: tuple(str, str)
        :param secure: If *credentials* is not none then can be set to a tuple
                       to enable encryption for the connection to the SMTP
                       server.  The tuple can follow one of three forms, an
                       empty tuple *()*, a single value tuple with the name of
                       a keyfile *(keyfile,)*, or a 2-value tuple with the
                       names of a keyfile and certificate file *(keyfile,
                       certificatefile)*.  This is then passed to
                       :meth:`smtplib.SMTP.starttls`.
        :type secure: tuple
        :param timeout: A timeout (in seconds) for communications with the SMTP
                        server.
        :type timeout: float | int
        """

        BurinHandler.__init__(self)

        if isinstance(mailhost, (list, tuple)):
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost = mailhost
            self.mailport = None

        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None

        if isinstance(toaddrs, str):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.fromaddr = fromaddr
        self.secure = secure
        self.subject = subject
        self.timeout = timeout

    # Alias methods from the standard library handler
    get_subject = SMTPHandler.getSubject
