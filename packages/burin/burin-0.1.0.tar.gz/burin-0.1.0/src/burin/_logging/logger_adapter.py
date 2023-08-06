"""
Burin Logger Adapter

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Burin imports
from .._log_levels import CRITICAL, DEBUG, ERROR, INFO, WARNING, get_level_name


class BurinLoggerAdapter:
    """
    An adapter for easily passing contextual information in logging events.

    .. note::

        This differs slightly from the standard libraries
        :class:`logging.LoggerAdapter`.  Primarily the *extra* dictionary that
        is part of this adapter is merged with any *extra* dictionary that is
        part of each logging call instead of overwriting it.

        This allows for more use cases and better nesting functionality.  Also
        the *manager* property and *_log* method are not part of this class as
        they were unused.

    .. note::

        Almost all of the properties and non-logging methods of this class
        simply delegate to the underlying logger instance.

    Using an adapter can simplify logging calls where specific contextual
    information would repeatedly need to be added to logging calls by instead
    automatically adding that contextual information for every logging event.

    This is supported by essentially providing an *extra* value once when
    instantiating an adapter which is then added every time a logging method is
    called through the adapter.

    The *extra* mapping is added to the log record's *__dict__*, so this can
    allow custom fields in the format string used in a :class:`BurinFormatter`
    to be populated with these values.
    """

    def __init__(self, logger, extra=None):
        """
        Initialization requires a *logger* and the optional *extra* mapping.

        :param logger: The logger to use when calling logging events.
        :type logger: BurinLogger
        :param extra: The mapping to be added to the log record's *__dict__*.
        :type extra: dict{str: Any}
        """

        self.logger = logger
        self.extra = extra

    @property
    def msgStyle(self):
        """
        Gets or sets the :attr:`BurinLogger.msgStyle` of the underlying logger.

        See :attr:`BurinLogger.msgStyle` for more information about how this is
        used and what it can be set to.

        .. note::

            This will raise a :exc:`FactoryError` if it is set to a value that
            doesn't match with any log record factory.
        """

        return self.logger.msgStyle

    @msgStyle.setter
    def msgStyle(self, style):
        self.logger.msgStyle = style

    @property
    def name(self):
        """
        Gets the name of the underlying logger.

        This cannot be set through the adapter.
        """

        return self.logger.name

    def critical(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`CRITICAL` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLoggerAdapter.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.log(CRITICAL, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`DEBUG` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLoggerAdapter.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.log(DEBUG, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`ERROR` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLoggerAdapter.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.log(ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Logs a message with the :const:`ERROR` level with exception info.

        This should normally be called only within an exception handler.

        Additional arguments are interpreted the same way as
        :meth:`BurinLoggerAdapter.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.log(ERROR, msg, *args, exc_info=exc_info, **kwargs)

    def get_effective_level(self):
        """
        Gets the effective log level for the underlying logger.

        :returns: The effective log level for the underlying logger.
        :rtype: int
        """

        return self.logger.get_effective_level()

    def has_handlers(self):
        """
        Checks if there are any available handlers for the underlying logger.

        :returns: Whether the underlying logger has any available handlers.
        :rtype: bool
        """

        return self.logger.has_handlers()

    def info(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`INFO` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLoggerAdapter.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.log(INFO, msg, *args, **kwargs)

    def is_enabled_for(self, level):
        """
        Checks if the underlying logger is enabled for the specified *level*.

        :param level: The level to check on the underlying logger.
        :type level: int | str
        :returns: If the underlying logger is enabled for *level*.
        :rtype: bool
        """

        return self.logger.is_enabled_for(level)

    def log(self, level, msg, *args, **kwargs):
        """
        Logs a message with the specified *level*.

        .. note::

            Unlike :meth:`BurinLogger.log` all keyword arguments (like
            *exc_info*, *extra*, *stack_info*, and *stacklevel*) are just
            handled as *kwargs* instead of specific arguments.  This allows for
            more flexibility in any subclassed adapters as all of the *kwargs*
            are passed for processing as just a dictionary.

        This will call :meth:`BurinLoggerAdapter.process` to add the *extra*
        values of this adapter with the logging call before calling the
        underlying logger.

        Everything is passed to the underlying logger, so for more information
        about how it can be used and additional arguments please see
        :meth:`BurinLogger.log`.

        :param level: The level to log the message at.
        :type level: int | str
        :param msg: The message to log.
        :type msg: str
        """

        if self.is_enabled_for(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger.log(level, msg, *args, **kwargs)

    def process(self, msg, kwargs):
        """
        Processes the log event for the adapter.

        This will add the *extra* values passed to the adapter when it was
        instantiated to the log event kwargs.  If another *extra* dictionary
        was passed as part of the logging event then this will merge the
        *extra* values with the ones from the log event call taking precedence.

        This can be overridden to provide other types of processing or
        customised adapters.  The log *msg* and all *kwargs* from the logging
        call are passed in.

        :param msg: The log message.
        :type msg: str
        :param kwargs: All keyword arguments that were passed with the logging
                       call.
        :type kwargs: dict{str: Any}
        :returns: The log message and keyword arguments to be sent to the
                  underlying logger after processing.
        :rtype: tuple(str, dict{str: Any})
        """

        kwargs["extra"] = self.extra if kwargs["extra"] is None else {**self.extra, **kwargs["extra"]}
        return msg, kwargs

    def set_level(self, level):
        """
        Sets the level of the underlying logger.

        :param level: The new level for the handler.
        :type level: int | str
        """

        self.logger.set_level(level)

    def warning(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`WARNING` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLoggerAdapter.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.log(WARNING, msg, *args, **kwargs)

    def __repr__(self):
        logger = self.logger
        level = get_level_name(logger.get_effective_level())
        return f"<{self.__class__.__name__} {logger.name} ({level})>"

    # Aliases for better compatibility to replace standard library logging
    getEffectiveLevel = get_effective_level
    hasHandlers = has_handlers
    isEnabledFor = is_enabled_for
    setLevel = set_level
