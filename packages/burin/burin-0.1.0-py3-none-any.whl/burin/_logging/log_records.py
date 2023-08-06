"""
Burin Log Record

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python Imports
import collections
import os
from string import Template
import threading
import time
import sys

# Burin Imports
from .._log_levels import get_level_name
from .._state import logMultiprocessing, logProcesses, logThreads, _internals


logRecordFactories = {}


class BurinLogRecord:
    """
    Represents all of the values of a logging event.

    This will format log messages with any additional *args* using percent (%)
    style formatting.

    Custom log record factories that are created should inherit from this and
    typically only override the :meth:`BurinLogRecord.get_message` method.
    """

    #: This is the key used for the class as a log record factory.  This is
    #: updated automatically when the class is set using
    #: :func:`set_log_record_factory`.
    factoryKey = None

    def __init__(self, name, level, pathname, lineno, msg, args, exc_info,
                 func=None, sinfo=None, **kwargs):
        """
        This initializes the log record and stores all relevant values.

        Unlike the standard library :class:`logging.LogRecord` this also stores
        all extra *kwargs* that were not used in the logging call.   These can
        then be used later when formatting the log message.

        :param name: The name of the logger that was called.
        :type name: str
        :param level: The level for the log message.
        :type level: int
        :param pathname: The full pathname of the file where the logging call
                         was made.
        :type pathname: str
        :param lineno: The line number of where the logging call was made.
        :type lineno: int
        :param msg: The logging message.
        :type msg: str
        :param args: Additional positional arguments passed with the logging
                     call.
        :type args: tuple(Any) | None
        :param exc_info: Exception information related to the logging call.
        :type exc_info: tuple(type, Exception, traceback)
        :param func: The name of the function where the logging call was made.
        :type func: str
        :param sinfo: Text of the stack information from where the logging call
                      was made.
        :type sinfo: str
        """

        # Get the time the record is created
        recordTime = time.time()

        self.name = name
        self.msg = msg

        # This is to allow the passing of a dictionary as a sole argument to
        # allow for things like:
        #     burin.debug("a %(a)d b %(b)s", {'a': 1, 'b':2})
        # This is a feature of the Python standard library's LogRecord class
        # and is duplicated here (from Python 3.10.2) to provide a proper
        # replacement for as many use cases as possible
        if (args and len(args) == 1 and isinstance(args[0], collections.abc.Mapping) and args[0]):
            args = args[0]

        self.args = args
        self.kwargs = kwargs
        self.levelname = get_level_name(level)
        self.levelno = level
        self.exc_info = exc_info
        self.exc_text = None    # Used by BurinFormatter to cache traceback text
        self.stack_info = sinfo
        self.lineno = lineno
        self.funcName = func
        self.created = recordTime
        self.msecs = (recordTime - int(recordTime)) * 1000
        self.relativeCreated = (self.created - _internals["startTime"]) * 1000

        self.pathname = pathname
        try:
            self.filename = os.path.basename(pathname)
            self.module = os.path.splitext(self.filename)[0]
        except (TypeError, ValueError, AttributeError):
            self.filename = pathname
            self.module = "Unknown module"

        if logThreads:
            self.thread = threading.get_ident()
            self.threadName = threading.current_thread().name
        else:
            self.thread = None
            self.threadName = None

        if logMultiprocessing:
            self.processName = "MainProcess"
            multiProcessing = sys.modules.get("multiprocessing")
            if multiProcessing is not None:
                try:
                    self.processName = multiProcessing.current_process().name
                except Exception:
                    pass
        else:
            self.processName = None

        if logProcesses and hasattr(os, "getpid"):
            self.process = os.getpid()
        else:
            self.process = None

    def get_message(self):
        """
        This formats the log message.

        All additional *args* that were part of the log record creation are
        used for the formatting of the log message.

        :returns: The formatted log message.
        :rtype: str
        """

        msg = str(self.msg)
        if self.args:
            msg = msg % self.args
        return msg

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.levelno}, {self.pathname}, {self.lineno}, {self.msg}>"

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message


class BurinBraceLogRecord(BurinLogRecord):
    """
    A log record that will be formatted in :meth:`str.format` ({ style).

    This allows for deferred formatting using positional and/or keyword
    arguments that are passed in during log record creation.

    This is derived from :class:`BurinLogRecord`.
    """

    def get_message(self):
        """
        This formats the log message.

        All additional *args* and *kwargs* that were part of the log record
        creation are used for the formatting of the log message.

        :returns: The formatted log message.
        :rtype: str
        """

        msg = str(self.msg)
        if self.args or self.kwargs:
            msg = msg.format(*self.args, **self.kwargs)
        return msg

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message


class BurinDollarLogRecord(BurinLogRecord):
    """
    A log record that will be formatted in :class:`string.Template` ($ style).

    This allows for deferred formatting using keyword arguments that are passed
    in during log record creation.

    This is derived from :class:`BurinLogRecord`.
    """

    def get_message(self):
        """
        This formats the log message.

        All additional *kwargs* that were part of the log record creation are
        used for the formatting of the log message.

        :meth:`string.Template.safe_substitute` so no exceptions are raised
        if keys and format placeholders don't all match.

        :returns: The formatted log message.
        :rtype: str
        """

        msg = str(self.msg)
        if self.kwargs:
            msg = Template(msg).safe_substitute(self.kwargs)
        return msg

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message


# These functions allow customisation of the log records that are used
def get_log_record_factory(msgStyle="%"):
    """
    Gets the log record factory class for the specified style.

    If no log record factory exists for the *msgStyle* then **None** is
    returned.

    :param msgStyle: The style to get the associated log record factory for.
                     (Default = '%')
    :type msgStyle: str
    :returns: The log record factory class associated with the *msgStyle* or
              **None** if no factory exists for that style.
    :rtype: BurinLogRecord | None
    """

    try:
        return logRecordFactories[msgStyle]
    except KeyError:
        return None

def make_log_record(recordDict, msgStyle="%"):
    """
    Creates a new log record from a dictionary.

    This is intended for rebuilding log records that were pickled and sent
    over a socket.

    Typically *msgStyle* won't matter here as the msg formatting is done before
    a record is pickled and sent.  It is provided as a parameter here for
    special use cases.

    :param recordDict: The dictionary of the log record attributes.
    :type recordDict: dict{str: Any}
    :param msgStyle: The *msgStyle* of which log record factory to use when
                     rebuilding the record.  (Default = '%')
    :type msgStyle: str
    :returns: The reconstructed log record.
    :rtype: BurinLogRecord
    """

    logRecord = logRecordFactories[msgStyle](None, None, "", 0, "", (), None)
    logRecord.__dict__.update(recordDict)

    return logRecord

def set_log_record_factory(factory, msgStyle="%"):
    """
    Sets the log record class to use as a factory.

    The factory can be set to any type of *msgStyle*.  If a factory is already
    set for that *msgStyle* it is replaced, otherwise the new factory is simply
    added without impacting the other factories.

    Once a factory has been set to a *msgStyle* then the same style  can be
    used as the *msgStyle* on loggers to use that specific log record factory.

    :param factory: The new log record class to use as a factory.  This should
                    be a subclass of :class:`BurinLogRecord`.
    :type factory: BurinLogRecord
    :param msgStyle: The style and key used to reference the factory for
                     loggers.  (Default = '%')
    :type msgStyle: str
    """

    logRecordFactories[msgStyle] = factory
    factory.factoryKey = msgStyle


# Aliases for better compatibility to replace standard library logging
getLogRecordFactory = get_log_record_factory
makeLogRecord = make_log_record
setLogRecordFactory = set_log_record_factory


# Set the factories for the built-in record types
set_log_record_factory(BurinLogRecord, "%")
set_log_record_factory(BurinBraceLogRecord, "{")
set_log_record_factory(BurinDollarLogRecord, "$")
