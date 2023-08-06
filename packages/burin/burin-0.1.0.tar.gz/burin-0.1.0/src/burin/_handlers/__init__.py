"""
Burin Handlers

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import (DEFAULT_HTTP_LOGGING_PORT, DEFAULT_SOAP_LOGGING_PORT,
                              DEFAULT_TCP_LOGGING_PORT, DEFAULT_UDP_LOGGING_PORT,
                              SYSLOG_TCP_PORT, SYSLOG_UDP_PORT)

# Burin imports
from .._log_levels import WARNING

# Package Contents
from .base_rotating_handler import BurinBaseRotatingHandler
from .buffering_handler import BurinBufferingHandler
from .datagram_handler import BurinDatagramHandler
from .file_handler import BurinFileHandler
from .handler import BurinHandler
from .http_handler import BurinHTTPHandler
from .memory_handler import BurinMemoryHandler
from .nt_event_log_handler import BurinNTEventLogHandler
from .null_handler import BurinNullHandler
from .queue_handler import BurinQueueHandler
from .queue_listener import BurinQueueListener
from .rotating_file_handler import BurinRotatingFileHandler
from .smtp_handler import BurinSMTPHandler
from .socket_handler import BurinSocketHandler
from .stream_handler import BurinStreamHandler
from .syslog_handler import BurinSyslogHandler
from .timed_rotating_file_handler import BurinTimedRotatingFileHandler
from .watched_file_handler import BurinWatchedFileHandler
from ._references import _handlerList  # noqa: F401
from ._stderr_handler import _BurinStderrHandler


# The last resort if no other handlers are set
lastResort = _BurinStderrHandler(WARNING)


__all__ = ["DEFAULT_HTTP_LOGGING_PORT", "DEFAULT_SOAP_LOGGING_PORT",
           "DEFAULT_TCP_LOGGING_PORT", "DEFAULT_UDP_LOGGING_PORT",
           "SYSLOG_TCP_PORT", "SYSLOG_UDP_PORT", "BurinBaseRotatingHandler",
           "BurinBufferingHandler", "BurinDatagramHandler", "BurinFileHandler",
           "BurinHandler", "BurinHTTPHandler", "BurinMemoryHandler",
           "BurinNTEventLogHandler", "BurinNullHandler", "BurinQueueHandler",
           "BurinQueueListener", "BurinRotatingFileHandler", "BurinSMTPHandler",
           "BurinSocketHandler", "BurinStreamHandler", "BurinSyslogHandler",
           "BurinTimedRotatingFileHandler", "BurinWatchedFileHandler",
           "lastResort"]


# Clean up some things that aren't part of this package
del WARNING
