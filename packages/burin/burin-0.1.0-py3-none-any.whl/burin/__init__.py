"""
Burin Logging Package

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

__author__ = "William Foster"
__license__ = "BSD-3-Clause"
__title__ = "Burin"
__version__ = "0.1.0"


# Package imports
from ._burin import (critical, debug, disable, error, exception, info, log,
                     shutdown, warning)
from ._config import basic_config, basicConfig
from ._exceptions import ConfigError, FactoryError, FormatError
from ._formatters import BurinBufferingFormatter, BurinFormatter
from ._handlers import (BurinBaseRotatingHandler, BurinBufferingHandler,
                        BurinDatagramHandler, BurinFileHandler, BurinHandler,
                        BurinHTTPHandler, BurinMemoryHandler,
                        BurinNTEventLogHandler, BurinNullHandler,
                        BurinQueueHandler, BurinQueueListener,
                        BurinRotatingFileHandler, BurinSMTPHandler,
                        BurinSocketHandler, BurinStreamHandler,
                        BurinSyslogHandler, BurinTimedRotatingFileHandler,
                        BurinWatchedFileHandler)
from ._log_levels import (CRITICAL, DEBUG, ERROR, INFO, WARNING,
                          get_level_name, getLevelName)
from ._logging import (BurinBraceLogRecord, BurinDollarLogRecord,
                       BurinLogRecord, BurinLogger, BurinLoggerAdapter,
                       get_logger, getLogger, get_log_record_factory,
                       getLogRecordFactory, get_logger_class, getLoggerClass,
                       make_log_record, makeLogRecord, set_log_record_factory,
                       setLogRecordFactory, set_logger_class, setLoggerClass)
from ._state import (logMultiprocessing, logProcesses, logThreads,
                     raiseExceptions)
from ._warnings import capture_warnings, captureWarnings


__all__ = ["critical", "debug", "disable", "error", "exception", "info", "log",
           "shutdown", "warning", "basic_config", "basicConfig", "ConfigError",
           "FactoryError", "FormatError", "BurinBufferingFormatter",
           "BurinFormatter", "BurinBaseRotatingHandler",
           "BurinBufferingHandler", "BurinDatagramHandler", "BurinFileHandler",
           "BurinHandler", "BurinHTTPHandler", "BurinMemoryHandler",
           "BurinNTEventLogHandler", "BurinNullHandler", "BurinQueueHandler",
           "BurinQueueListener", "BurinRotatingFileHandler", "BurinSMTPHandler",
           "BurinSocketHandler", "BurinStreamHandler", "BurinSyslogHandler",
           "BurinTimedRotatingFileHandler", "BurinWatchedFileHandler",
           "CRITICAL", "DEBUG", "ERROR", "INFO", "WARNING", "get_level_name",
           "getLevelName", "BurinBraceLogRecord", "BurinDollarLogRecord",
           "BurinLogRecord", "BurinLogger", "BurinLoggerAdapter", "get_logger",
           "getLogger", "get_log_record_factory", "getLogRecordFactory",
           "get_logger_class", "getLoggerClass", "make_log_record",
           "makeLogRecord", "set_log_record_factory", "setLogRecordFactory",
           "set_logger_class", "setLoggerClass", "logMultiprocessing",
           "logProcesses", "logThreads", "raiseExceptions", "capture_warnings",
           "captureWarnings"]
