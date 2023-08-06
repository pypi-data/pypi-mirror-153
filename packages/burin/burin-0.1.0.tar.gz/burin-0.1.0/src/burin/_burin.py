"""
Burin Logging General Functions

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python import
import atexit

# Burin imports
from ._config import basic_config
from ._handlers import _handlerList
from ._log_levels import CRITICAL, DEBUG, ERROR, INFO, WARNING, _check_level
from ._logging import get_logger, root
from ._state import raiseExceptions, _set_src_dir


# General logging calls that don't require a specific logger
def critical(msg, *args, logger=None, **kwargs):
    """
    Logs a message with the :const:`CRITICAL` level.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    Additional arguments are interpreted the same way as :func:`log`.

    :param msg: The message to log.
    :type msg: str
    :param logger: The name of the logger to log the event with.
    :type logger: str
    """

    log(CRITICAL, msg, *args, logger=logger, **kwargs)

def debug(msg, *args, logger=None, **kwargs):
    """
    Logs a message with the :const:`DEBUG` level.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    Additional arguments are interpreted the same way as :func:`log`.

    :param msg: The message to log.
    :type msg: str
    :param logger: The name of the logger to log the event with.
    :type logger: str
    """

    log(DEBUG, msg, *args, logger=logger, **kwargs)

def error(msg, *args, logger=None, **kwargs):
    """
    Logs a message with the :const:`ERROR` level.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    Additional arguments are interpreted the same way as :func:`log`.

    :param msg: The message to log.
    :type msg: str
    :param logger: The name of the logger to log the event with.
    :type logger: str
    """

    log(ERROR, msg, *args, logger=logger, **kwargs)

def exception(msg, *args, exc_info=True, logger=None, **kwargs):
    """
    Logs a message with the :const:`ERROR` level and exception information.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    This should normally be called only within an exception handler.

    Additional arguments are interpreted the same way as :func:`log`.

    :param msg: The message to log.
    :type msg: str
    :param logger: The name of the logger to log the event with.
    :type logger: str
    """

    log(ERROR, msg, exc_info=exc_info, logger=logger, **kwargs)

def info(msg, *args, logger=None, **kwargs):
    """
    Logs a message with the :const:`INFO` level.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    Additional arguments are interpreted the same way as :func:`log`.

    :param msg: The message to log.
    :type msg: str
    :param logger: The name of the logger to log the event with.
    :type logger: str
    """

    log(INFO, msg, *args, logger=logger, **kwargs)

def log(level, msg, *args, exc_info=None, extra=None, logger=None,
        stack_info=False, stacklevel=1, **kwargs):
    """
    Logs a message with the specified *level*.

    .. note::

        The arguments *exc_info*, *extra*, *logger*, *stack_info*, and
        *stacklevel* are all keyword only arguments.  These cannot be passed as
        positional arguments.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    Any additional *args* and *kwargs* will be kept with the message and
    used for deferred formatting before output.  Deferred formatting allows
    you to pass in a format string for the message and the values as
    additional arguments.  The message then will only be formatted if it is
    going to be emitted by a handler.

    How this formatting is done is determined by the log record factory
    used.  This is controlled by the :attr:`BurinLogger.msgStyle` property
    of the logger.  See :meth:`BurinLogger.log` for examples of the different
    *msgStyle* deferred formatting options.

    Additional or customised log record factories can be used by adding them
    with the :func:`set_log_record_factory` function.

    :param level: The level to log the message at.
    :type level: int | str
    :param msg: The message to log.
    :type msg: str
    :param exc_info: Exception information to be added to the logging
                     message.  This should be an exception instance or an
                     exception tuple (as returned by :func:`sys.exc_info`)
                     if possible; otherwise if it is any other value that
                     doesn't evaluate as **False** then the exception
                     information will be fetched using
                     :func:`sys.exc_info`.
    :type exc_info: Exception | tuple(type, Exception, traceback) | bool
    :param extra: A dictionary of extra attributes that are applied to the
                  log record's *__dict__*.  These can be used to populate
                  custom fields that you set in your format string for
                  :class:`BurinFormatter`.  The keys in this dictionary
                  must not interfere with the built in fields/keys in the
                  log record.
    :type extra: dict{str: Any}
    :param logger: The name of the logger to log the event with.  By default
                   and when this is **None** then the root logger is used.  If
                   this is not **None** and the named logger doesn't exist then
                   it is created first.
    :type logger: str
    :param stack_info: Whether to get the stack information from the
                       logging call and add it to the log record.  This
                       allows for getting stack information for logging
                       without an exception needing to be raised.  (Default
                       = **False**)
    :type stack_info: bool
    :param stacklevel: If this is greater than 1 then the corresponding
                       number of stack frames are skipped back through when
                       getting the logging caller's information (like
                       filename, lineno, and funcName).  This can be useful
                       when the log call was from helper/wrapper code that
                       doesn't need to be included in the log record.
    :type stacklevel: int
    :raises KeyError: If any key in *extra* conflicts with a built in key
                      of the log record.
    """

    if logger is None or logger == root.name:
        logger = root

        if not root.has_handlers():
            basic_config()
    else:
        logger = get_logger(logger)

    logger.log(level, msg, *args, exc_info=exc_info, extra=extra,
               stack_info=stack_info, stacklevel=stacklevel, **kwargs)

def warning(msg, *args, logger=None, **kwargs):
    """
    Logs a message with the :const:`WARNING` level.

    A specific logger can be used passing its name with the *logger* keyword
    argument; otherwise the root logger is used.

    Additional arguments are interpreted the same way as :func:`log`.

    :param msg: The message to log.
    :type msg: str
    :param logger: The name of the logger to log the event with.
    :type logger: str
    """

    log(WARNING, msg, *args, logger=logger, **kwargs)


# Set the directory of Burin which is used in traceback checks
_set_src_dir(log)


# Disable all logging of a specific level and below
def disable(level="CRITICAL"):
    """
    Provides a way to easily disable a level for all loggers.

    This can be helpful for situations where you need to throttle logging
    output throughout an entire application quickly.

    All logging events of *level* or below will not be processed.

    To reset this back to normal it can simply be called again with
    :const:`NOTSET` as *level*.

    :param level: The level where all logging events and below should not be
                  processed.  (Default = "CRITICAL")
    :type level: int | str
    """

    root.manager.disable = _check_level(level)
    root.manager._clear_cache()


# Logging should be shutdown properly before the program exits
def shutdown(handlerList=None):
    """
    Cleans up by flushing and closing all handlers.

    This is automatically registered with :func:`atexit.register` and therefore
    shouldn't need to be called manually when an application closes.

    :param handlerList: The handlers to be cleaned up.  If this is **None**
                        then it will default to an internal list of all Burin
                        handlers.  This should not need to be changed in almost
                        all circumstances.  However; if you only want to clean
                        up a specific set of handlers then pass them here.
    :type handlerList: list[BurinHandler]
    """

    if handlerList is None:
        handlerList = _handlerList

    # Go through a copy of the handler list
    for handlerWeakRef in reversed(handlerList[:]):
        try:
            # The weakref callback should remove the handler from the list
            handler = handlerWeakRef()

            # Cleanup the handler
            if handler:
                try:
                    handler.acquire()
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    # Ignore errors that might be from a handler already being
                    # closed but still having references when the application
                    # exits
                    pass
                finally:
                    handler.release()
        except:  # noqa: E722
            # Ignore unless we're raising exceptions
            if raiseExceptions:
                raise


# Try to ensure shutdown called automatically on exit
atexit.register(shutdown)
