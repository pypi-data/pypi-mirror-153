"""
Burin Logger

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python Imports
from logging import Filterer
import io
import os.path
import sys
import traceback

# Burin Imports
from .._exceptions import FactoryError
from .._handlers import lastResort
from .._log_levels import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, get_level_name, _check_level
from .._state import raiseExceptions, _internals
from .._threading import _BurinLock
from .log_records import logRecordFactories


# Setup a way to get the current frame
if hasattr(sys, "_getframe"):
    def current_frame():
        return sys._getframe(3)
else:
    def current_frame():
        """
        Return the frame object for the caller's stack frame.

        :returns: The current frame from the caller's stack.
        :rtype:
        """

        # Intentionally raise an exception to get a frame from the exc_info
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back

# This is the general function for getting a logger instance from Burin
def get_logger(name=None, msgStyle=None):
    """
    Get a logger with the specified name and msgStyle.

    If *name* is **None** then the root logger will be returned.  Otherwise it
    will try to find any previously created logger with the specified *name*.

    If no existing logger with *name* is found then a new :class:`BurinLogger`
    instance is created with that *name*.  When creating a new logger if
    *msgStyle* is **None** then the *msgStyle* of the root logger will be used.

    A *name* can be any almost text value the developer likes.  Any periods '.'
    within the names though will be treated as separators for a hierarchy of
    loggers.  For example a name of 'a.b.c' will get or create logger 'a.b.c'
    which is a child of logger 'a.b'; logger 'a.b' is also a child of logger
    'a'. Any parts of the hierarchy that don't exist already are constructed
    with placeholder classes that are replaced with actual loggers if ever
    fetched by name.

    Children in the hierarchy typically propagate logging events up to parents
    which allows for handlers further up the hierarchy to emit these log
    records.

    If *msgStyle* is not **None** then it will be set as the *msgStyle* on the
    retrieved logger.  If this is the root logger then that will become the
    default *msgStyle* for all new loggers created afterwards.

    :param name: The name of the logger the get.  If this logger doesn't exist
                 already then it will be created.  If this is **None** then the
                 root logger will be returned.
    :type name: str
    :param msgStyle: If this is not **None** then it is set as the *msgStyle*
                     on the retrieved logger.  If that is the root logger then
                     this will also change the default *msgStyle* for any new
                     loggers created afterwards.  Built in possible values are
                     '%' for %-formatting, '{' for :meth:`str.format`
                     formatting, and '$' for :class:`string.Template`
                     formatting.  Other values can be used if custom log record
                     factories are added using :func:`set_log_record_factory`.
    :type msgstyle: str
    :returns: The logger with the specified *name*.
    :rtype: BurinLogger
    :raises FactoryError: If *msgStyle* doesn't match any known log record
                          factory.
    """

    # Default to the root logger which should be initialized at the end of this
    # module
    if name is None or (isinstance(name, str) and name == root.name):
        if msgStyle is not None and msgStyle != root.msgStyle:
            root.msgStyle = msgStyle

        return root

    # This relies on the manager having been initialized and set which should
    # occur when the _logging package is initialized.
    return BurinLogger.manager.get_logger(name, msgStyle)


# Aliases for better compatibility to replace standard library logging
getLogger = get_logger


class BurinLogger(Filterer):
    """
    Loggers represent a logging channel within an application.

    .. note::

        While this is based off :class:`logging.Logger` it is not a subclass of
        it and has a few differences and additions.

        Deprecated methods like :meth:`logging.Logger.warn` or
        :meth:`logging.Logger.fatal` do not exist as methods for this class.

        Other methods from :class:`logging.Logger` can be called in the same
        way on this class without using any of the changes if desired.

    This should never be instantiated directly during normal use; instead
    always use the :func:`get_logger` function instead to create a new
    instance.  Calling :func:`get_logger` with the same name will always return
    the same logger instance.

    What a logging channel encompasses is normally a specific area of the
    software and is up to each developer; it could be a class, module, package,
    process, etc.

    Typically the name of the logger matches the area the logging channel
    represents; for example a common use case is ``burin.get_logger(__name__)``
    which uses the module name for the logger.

    BurinLoggers support a hierarchy similar to Python packages; so any periods
    '.' within a name represent multiple steps.  An example is the name
    'foo.bar.baz' which shows three different loggers at different places in
    the hierarchy.  The logger 'foo' is higher up the hierarchy and is a parent
    of 'foo.bar', and then 'foo.bar' is subsquently a parent of 'foo.bar.baz'.

    Children can propagate logging events up to parents above them in the
    hierarchy.  This can simplify how handlers are setup as each logger doesn't
    need to have its own handlers added if somewhere up the line a parent has
    the desired handlers already attached.
    """

    # This should be set during _logging package initialization
    manager = None

    def __init__(self, name, level="NOTSET", msgStyle="%"):
        """
        Initialization of the logger sets it up to start processing log events.

        :param name: The name of the logger.
        :type name: str
        :param level: The logging level for the logger.  (Default = 'NOTSET')
        :type level: int | str
        :param msgStyle: The style of deferred formatting to use for log
                         messages.  This determines the log record factory that
                         is used when creating a new log record.  Built in
                         possible values are '%' for %-formatting, '{' for
                         :meth:`str.format` formatting, and '$' for
                         :class:`string.Template` formatting.  Other values can
                         be used if custom log record factories are added using
                         :func:`set_log_record_factory`. (Default = '%')
        :type msgStyle: str
        :raises FactoryError: If *msgStyle* doesn't match any known log record
                              factory.
        """

        Filterer.__init__(self)
        self.name = name
        self.level = _check_level(level)
        self.__msgStyle = None
        self.msgStyle = msgStyle
        self.parent = None
        self.propagate = True
        self.handlers = []
        self.disabled = False
        self._cache = {}

    @property
    def msgStyle(self):
        """
        Determines the log record factory to use when creating new log records.

        Built in possible values are '%' for %-formatting, '{' for
        :meth:`str.format` formatting, and '$' for :class:`string.Template`
        formatting.  Other values can be used if custom log record factories
        are added using :func:`set_log_record_factory`.

        .. note::

            This will raise a :exc:`FactoryError` if it is set to a value that
            doesn't match with any log record factory.
        """

        return self.__msgStyle

    @msgStyle.setter
    def msgStyle(self, style):
        if style not in logRecordFactories:
            raise FactoryError(f"style {style!r} is not associated with a known "
                               f"logRecordFactory: {', '.join(logRecordFactories.keys())}")

        self.__msgStyle = style

    # Alias methods from the standard library filterer
    add_filter = Filterer.addFilter
    remove_filter = Filterer.removeFilter

    def add_handler(self, handler):
        """
        Add the specified *handler* to this logger.

        :param handler: The handler to add to the logger.
        :type handler: BurinHandler
        """

        with _BurinLock:
            if handler not in self.handlers:
                self.handlers.append(handler)

    def call_handlers(self, record):
        """
        Passes a log record to all relevant handlers.

        This will call all handlers on this logger and then will move through
        parent loggers in the hierarchy calling their handlers based on
        propagation checks.

        :param record: The log record to pass to the handlers.
        :type record: BurinLogRecord
        """

        logger = self
        handlersFound = 0

        # Propagate through any parents to this logger.
        while logger:
            for handler in logger.handlers:
                handlersFound += 1

                if record.levelno >= handler.level:
                    handler.handle(record)

            if not logger.propagate:
                logger = None
            else:
                logger = logger.parent

        # Use a basic last resort handler if no others were found.
        if handlersFound == 0:
            if lastResort:
                if record.levelno >= lastResort.level:
                    lastResort.handle(record)
            elif raiseExceptions and not self.manager.emittedNoHandlerWarning:
                sys.stderr.write("No handlers could be found for logger "
                                 f"'{self.name}'")
                self.manager.emittedNoHandlerWarning = True

    def critical(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`CRITICAL` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLogger.log`.

        :param msg: The message to log.
        :type msg: str
        """

        if self.is_enabled_for(CRITICAL):
            self._log(CRITICAL, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`DEBUG` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLogger.log`.

        :param msg: The message to log.
        :type msg: str
        """

        if self.is_enabled_for(DEBUG):
            self._log(DEBUG, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`ERROR` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLogger.log`.

        :param msg: The message to log.
        :type msg: str
        """

        if self.is_enabled_for(ERROR):
            self._log(ERROR, msg, args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Logs a message with the :const:`ERROR` level and exception information.

        This should normally be called only within an exception handler.

        Additional arguments are interpreted the same way as
        :meth:`BurinLogger.log`.

        :param msg: The message to log.
        :type msg: str
        """

        self.error(msg, exc_info=exc_info, **kwargs)

    def find_caller(self, stack_info=False, stacklevel=1):
        """
        Finds the logging event caller's information.

        This will traverse back through frames until it is outside of the Burin
        library to find the caller of the logging event.

        This will get the filename, line number, function name, and optionally
        the stack information of the caller.

        :param stack_info: Whether the caller's stack information should be
                           returned as well.  (Default = **False**)
        :type stack_info: bool
        :param stacklevel: Allows stepping further back through stack frames in
                           case the log call was from helper/wrapper code that
                           should be ignored as well.
        :type stacklevel: int
        :returns: A tuple of the filename, line number, function name, and if
                  *stack_info*=**True** the stack information.
        :rtype: tuple(str, int, str, str | None)
        """

        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames
        frame = current_frame()

        if frame is not None:
            frame = frame.f_back
        originalFrame = frame

        # Ignore frames that originate within Burin
        srcDir = _internals["srcDir"]
        while hasattr(frame, "f_code"):
            if frame and srcDir in os.path.normcase(frame.f_code.co_filename):
                frame = frame.f_back
            else:
                break

        # If we have a frame reset the original; otherwise use the original
        if frame:
            originalFrame = frame
        else:
            frame = originalFrame

        # Move backwards through the frame stack to the desired level
        while frame and stacklevel > 1:
            frame = frame.f_back
            stacklevel -= 1

        # If we went back to far use the original frame
        if not frame:
            frame = originalFrame

        # Setup default caller info
        callerInfo = ("(unknown file)", 0, "(unknown function)", None)

        # Try to get the actual caller info
        if hasattr(frame, "f_code"):
            codeObject = frame.f_code

            # Get the stack info for the frame
            frameStackInfo = None
            if stack_info:
                stackIO = io.StringIO()
                stackIO.write("Stack (most recent call last):\n")
                traceback.print_stack(frame, file=stackIO)
                frameStackInfo = stackIO.getvalue()
                if frameStackInfo[-1] == "\n":
                    frameStackInfo = frameStackInfo[:-1]
                stackIO.close()

            callerInfo = (codeObject.co_filename, frame.f_lineno,
                          codeObject.co_name, frameStackInfo)

        return callerInfo

    def get_child(self, suffix):
        """
        Gets a child of this logger.

        The suffix can have multiple steps down the hierarchy by including
        additional period separate names '.'; this will all be added as
        descendants of this logger instance.

        Calling ``burin.get_logger('abc').get_child('def.ghi')`` would return
        the exact same logger as ``burin.get_logger('abc.def.ghi')``.

        If the requested logger already exists it is simply retrieved;
        otherwise it will be created.

        :param suffix: The part of the child logger's name below this logger.
        :type suffix: str
        :returns: The child logger.
        :rtype: BurinLogger
        """

        if self.root is not self:
            suffix = ".".join((self.name, suffix))

        return self.manager.get_logger(suffix, msgStyle=self.msgStyle)

    def get_effective_level(self):
        """
        Gets the effective log level for this logger.

        This will check if a specific level is set on this logger and if not
        then it will check through its parents until it finds one.  If no
        specific level is found then :const:`NOTSET` is returned.

        :returns: The effective log level for this logger.
        :rtype: int
        """

        logger = self

        # Find the level either for this logger or its parents if this doesn't
        # have a set one.
        while logger:
            if logger.level:
                return logger.level

            logger = logger.parent

        return NOTSET

    def handle(self, record):
        """
        Calls handlers for the record.

        This will check if the logger is disabled or any filters before calling
        handlers.

        :param record: The log record to pass to the handlers.
        :type record: BurinLogRecord
        """

        if not self.disabled and self.filter(record):
            self.call_handlers(record)

    def has_handlers(self):
        """
        Checks if there are any available handlers for this logger.

        This will check this logger and if it doesn't find any handlers it will
        move through parent loggers in the hierarchy looking for handlers
        based on propagation checks.

        :returns: Whether this logger has any available handlers.
        :rtype: bool
        """

        logger = self
        hasHandlers = False

        # Check for handlers on self and parents if propagation is enabled.
        while logger:
            if logger.handlers:
                hasHandlers = True
                break
            elif not logger.propagate:
                break
            else:
                logger = logger.parent

        return hasHandlers

    def info(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`INFO` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLogger.log`.

        :param msg: The message to log.
        :type msg: str
        """

        if self.is_enabled_for(INFO):
            self._log(INFO, msg, args, **kwargs)

    def is_enabled_for(self, level):
        """
        Checks if the logger is enabled for the specified *level*.

        :param level: The level to check on the logger.
        :type level: int | str
        :returns: If the logger is enabled for *level*.
        :rtype: bool
        """

        if self.disabled:
            return False

        level = _check_level(level)

        # Try to check for a cached check value for the level
        try:
            return self._cache[level]
        except KeyError:
            with _BurinLock:
                # Level isn't in cache so check if that level is disabled
                if self.manager.disable >= level:
                    isEnabled = self._cache[level] = False
                else:
                    # Not disabled so check self and potentially parents
                    isEnabled = self._cache[level] = level >= self.get_effective_level()

            return isEnabled

    def log(self, level, msg, *args, exc_info=None, extra=None,
            stack_info=False, stacklevel=1, **kwargs):
        """
        Logs a message with the specified *level*.

        .. note::

            The arguments *exc_info*, *extra*, *stack_info*, and *stacklevel*
            are all keyword only arguments.  These cannot be passed as
            positional arguments.

        Any additional *args* and *kwargs* will be kept with the message and
        used for deferred formatting before output.  Deferred formatting allows
        you to pass in a format string for the message and the values as
        additional arguments.  The message then will only be formatted if it is
        going to be emitted by a handler.

        How this formatting is done is determined by the log record factory
        used.  This is controlled by the :attr:`BurinLogger.msgStyle` property
        of the logger.  See examples below.

        % style:

        .. code-block:: python

            # Positional format args
            logger.log('DEBUG', 'This is a %s event in %s', 'DEBUG', 'Burin')
            # Keyword format args in a dictionary
            logger.log('DEBUG', 'This is a %(lvl)s event in %(prog)s',
                       { 'lvl': 'DEBUG', 'prog': 'Burin'})

        { :meth:`str.format` style:

        .. code-block:: python

            # Positional format args
            logger.log('DEBUG', 'This is a {} event in {}', 'DEBUG', 'Burin')
            # Format args as keyword args
            logger.log('DEBUG', 'This is a {lvl} event in {prog}', lvl='DEBUG',
                       prog='Burin')

        $ :class:`string.Template` style:

        .. code-block:: python

            # Format args as keyword args
            logger.log('DEBUG', 'This is a ${lvl} event in ${prog}',
                       lvl='DEBUG', prog='Burin')

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

        # Allow the level to be an int or a string.
        level = _check_level(level)

        if self.is_enabled_for(level):
            self._log(level, msg, args, exc_info=exc_info, extra=extra,
                      stack_info=stack_info, stacklevel=stacklevel, **kwargs)

    def make_record(self, name, level, fn, lno, msg, args, exc_info, func=None,
                    extra=None, sinfo=None, **kwargs):
        """
        Creates the log record and applies any extra fields to it.

        The type of log record that is created is determined by this logger's
        :attr:`BurinLogger.msgStyle` value.

        :param name: The name of the logger.
        :type name: str
        :param level: The level of the logging event.
        :type level: int
        :param fn: The filename of the log event caller.
        :type fn: str
        :param lno: The line number where the log event was called.
        :type lno:
        :param msg: The log message.
        :type msg: str
        :param args: The additional positional arguments for the log event
                     call.
        :type args: tuple(Any)
        :param exc_info: The exception information if this log event is from
                         an exception handler.
        :type exc_info: tuple(type, Exception, traceback)
        :param func: The name of the function where the log event was called.
        :type func: str
        :param extra: Extra fields to be applied to the log record.
        :type extra: dict{str: Any}
        :param sinfo: The stack information for the log event call.
        :type sinfo: str
        :returns: The newly created log record.
        :rtype: BurinLogRecord
        """

        # Get the record using the appropriate factory for msgStyle
        record = logRecordFactories[self.msgStyle](name, level, fn, lno, msg,
                                                   args, exc_info, func, sinfo,
                                                   **kwargs)

        # Add extras and ensure no reserved fields are overwritten
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in record.__dict__):
                    raise KeyError(f"Attempt to overwrite {key} in LogRecord")

                record.__dict__[key] = extra[key]

        return record

    def remove_handler(self, handler):
        """
        Removes the specified *handler* from this logger.

        :param handler: The handler to remove from the logger.
        :type handler: BurinHandler
        """

        with _BurinLock:
            if handler in self.handlers:
                self.handlers.remove(handler)

    def set_level(self, level):
        """
        Sets the level of this logger.

        :param level: The new level for the handler.
        :type level: int | str
        """

        self.level = _check_level(level)

        # Cached values may not be valid anymore so clear them all
        self.manager._clear_cache()

    def warning(self, msg, *args, **kwargs):
        """
        Logs a message with the :const:`WARNING` level.

        Additional arguments are interpreted the same way as
        :meth:`BurinLogger.log`.

        :param msg: The message to log.
        :type msg: str
        """

        if self.is_enabled_for(WARNING):
            self._log(WARNING, msg, args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False, stacklevel=1, **kwargs):
        """
        Internal method that actually processes the logging request.

        This will get the caller information, process the *exc_info* if its not
        **None**, make the log record, and then handle the record.

        This should only be called internally by other methods of
        :class:`BurinLogger`.  Most of the arguments are the same as
        :meth:`BurinLogger.log`.

        :param level: The level to log the message at.
        :type level: int | str
        :param msg: The message to log.
        :type msg: str
        :param args: Additional positional arugments that were passed by the
                     log event caller.  These can be used for deferred
                     formatting of the log message.
        :type args: tuple(Any) | None
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

        sinfo = None

        if _internals["srcDir"]:
            # IronPython doesn't track Python frames so find_caller raises an
            # exception in some versions, that is trapped here
            try:
                filename, lineno, func, sinfo = self.find_caller(stack_info,
                                                                 stacklevel)
            except ValueError:
                filename, lineno, func = ("(unknown file)", 0, "(unknown function)")
        else:
            filename, lineno, func = ("(unknown file)", 0, "(unknown function)")

        # Get the exception info if needed
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        # Make the log record
        record = self.make_record(self.name, level, filename, lineno, msg, args,
                                  exc_info, func, extra, sinfo, **kwargs)

        self.handle(record)

    def __repr__(self):
        level = get_level_name(self.get_effective_level())
        return f"<{self.__class__.__name__} {self.name} ({level})>"

    def __reduce__(self):
        if get_logger(self.name) is not self:
            import pickle
            raise pickle.PicklingError("logger cannot be pickled")

        return get_logger, (self.name,)

    # Aliases for better compatibility to replace standard library logging
    addHandler = add_handler
    callHandlers = call_handlers
    findCaller = find_caller
    getChild = get_child
    getEffectiveLevel = get_effective_level
    hasHandlers = has_handlers
    isEnabledFor = is_enabled_for
    makeRecord = make_record
    removeHandler = remove_handler
    setLevel = set_level


class _BurinRootLogger(BurinLogger):
    """
    There is only one root logger instance.

    The root logger is mostly identical to a normal :class:`BurinLogger`.  The
    only differences are that its name is always 'root' and the root logger's
    :attr:`_BurinRootLogger.msgStyle` is used as the default *msgStyle* for
    new loggers.
    """

    def __init__(self, level="WARNING", msgStyle="%"):
        """
        The root logger is automatically created within Burin.

        Only one root logger is needed and it is always at the top of the
        logger hierarchy.

        :param level: The logging level for the logger.  (Default = 'WARNING')
        :type level: int | str
        :param msgStyle: The style of deferred formatting to use for log
                         messages.  This determines the log record factory that
                         is used when creating a new log record.  Also when
                         this is set on the root logger it changes the default
                         *msgStyle* for new loggers.  Built in possible values
                         are '%' for %-formatting, '{' for :meth:`str.format`
                         formatting, and '$' for :class:`string.Template`
                         formatting.  Other values can be used if custom log
                         record factories are added using
                         :func:`set_log_record_factory`. (Default = '%')
        :type msgStyle: str
        :raises FactoryError: If *msgStyle* doesn't match any known log record
                              factory.
        """

        BurinLogger.__init__(self, "root", level, msgStyle)

    def __reduce__(self):
        return get_logger, ()


# Setup the root logger
root = _BurinRootLogger(WARNING)
BurinLogger.root = root
