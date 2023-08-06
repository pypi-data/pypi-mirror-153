"""
Burin Manager

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Burin Imports
from .._threading import _BurinLock
from .._log_levels import _check_level
from .log_records import logRecordFactories
from .logger import BurinLogger


class _BurinPlaceholder:
    """
    Acts as a placeholder within the logger hierarchy.

    .. note::

        This functions identically to the standard library
        :class:`logging.Placeholder` class.

    This is used to ensure that the logger hierarchy is fully populated when
    parents of other loggers haven't been created.
    """

    def __init__(self, childLogger):
        """
        The placeholder is created an internal map with the child logger.

        :param childLogger: A logger or another placeholder that is a child of
                            this within the logger hierarchy.
        :type childLogger: BurinLogger | _BurinPlaceholder
        """

        self.loggerMap = { childLogger: None }  # noqa: E201, E202

    def append(self, childLogger):
        """
        Adds the specified logger as another child.

        :param childLogger: A logger or another placeholder that is a child of
                            this within the logger hierarchy.
        :type childLogger: BurinLogger | _BurinPlaceholder
        """


class _BurinManager:
    """
    Manages the logger hierarchy and creating new loggers.

    .. note::

        This works similarly to the standard library :class:`logging.Manager`,
        but there are a few key differences for Burin.  Since this is intended
        for internal use only there are some missing methods or new properties
        compared to the standard library that were unused within Burin.

    Typically there should only even be one manager instance.
    """

    _disable = 0
    _logRecordFactory = None
    _loggerClass = None

    def __init__(self, rootLogger, loggerClass=BurinLogger):
        """
        This creates the manager instance.

        The :attr:`_BurinManager.logRecordFactory` is set based on the
        *msgStyle* property of the root logger.

        :param rootLogger: The root logger that is at the top of the logger
                           hierarchy.
        :type rootLogger: _BurinRootLogger
        :param loggerClass: The class that is used to create new loggers.  This
                            must be derived from :class:`BurinLogger`.
        :type loggerClass: BurinLogger
        :raises TypeError: If *loggerClass* is a class that is not a subclass
                           of :class:`BurinLogger`.
        """

        self.root = rootLogger
        self.loggerClass = loggerClass
        self.logRecordFactory = logRecordFactories[rootLogger.msgStyle]
        self.disable = 0
        self.emittedNoHandlerWarning = False
        self.loggerDict = {}

    @property
    def disable(self):
        """
        All logging is disabled for this level or below.

        This will always be an *int* when fetched, but it can be set as either
        an *int* or a *str*.
        """
        return self._disable

    @disable.setter
    def disable(self, value):
        self._disable = _check_level(value)

    @property
    def loggerClass(self):
        """
        The class that is used when instantiating new loggers.

        This will raise a :exc:`TypeError` if set to something that is not
        derived from :class:`BurinLogger`.
        """
        return self._loggerClass

    @loggerClass.setter
    def loggerClass(self, newClass):
        if not issubclass(newClass, BurinLogger):
            raise TypeError("logger is not a subclass of burin.BurinLogger: "
                            f"{newClass.__name__}")

        self._loggerClass = newClass

    def get_logger(self, name, msgStyle=None):
        """
        Get a logger with the specified name and msgStyle.

        If *name* is **None** then the root logger will be returned.  Otherwise
        it will try to find any previously created logger with the specified
        *name*.

        If no existing logger with *name* is found then a new logger instance
        is created with that *name*.  When creating a new logger if *msgStyle*
        is **None** then the *msgStyle* of the root logger will be used.

        If *msgStyle* is not **None** then it will be set as the *msgStyle* on
        the retrieved logger.  If this is the root logger then that will become
        the default *msgStyle* for all new loggers created afterwards.

        This shouldn't be called directly; instead the main :func:`get_logger`
        function should be called which will then call this method as needed.

        :param name: The name of the logger the get.  If this logger doesn't
                     exist already then it will be created.
        :type name: str
        :param msgStyle: If this is not **None** then it is set as the
                         *msgStyle* on the retrieved logger.  If that is the
                         root logger then this will also change the default
                         *msgStyle* for any new loggers created afterwards.
                         Built in possible values are '%' for %-formatting,
                         '{' for :meth:`str.format` formatting, and '$' for
                         :class:`string.Template` formatting.  Other values can
                         be used if custom log record factories are added using
                         :func:`set_log_record_factory`.
        :type msgstyle: str
        :returns: The logger with the specified *name*.
        :rtype: BurinLogger
        :raises FactoryError: If *msgStyle* doesn't match any known log record
                              factory.
        """

        logger = None

        if not isinstance(name, str):
            raise TypeError("A logger name must be a string")

        with _BurinLock:
            # Use the current default msgStyle for new loggers if none
            # is specified
            newMsgStyle = msgStyle if msgStyle is not None else self.root.msgStyle

            if name in self.loggerDict:
                logger = self.loggerDict[name]

                # If this was a placeholder then make it a real logger now
                if isinstance(logger, _BurinPlaceholder):
                    placeHolder = logger
                    logger = self._loggerClass(name, msgStyle=newMsgStyle)
                    logger.manager = self
                    self.loggerDict[name] = logger
                    self._fixup_children(placeHolder, logger)
                    self._fixup_parents(logger)
                else:
                    # If the logger's msgStyle is different that what was
                    # received then change it
                    if msgStyle is not None and msgStyle != logger.msgStyle:
                        logger.msgStyle = msgStyle
            else:
                # Create the logger if nothing was found
                logger = self._loggerClass(name, msgStyle=newMsgStyle)
                logger.manager = self
                self.loggerDict[name] = logger
                self._fixup_parents(logger)

        return logger

    def _fixup_parents(self, logger):
        """
        Ensures that the hierarchy above a logger is populated.

        The hierarchy above the specified *logger* is checked all the way up to
        the root logger.  It must be populated with other loggers or
        placeholders for loggers that haven't been created yet, so any gaps
        are filled with new placeholders.

        :param logger: The logger where everything above it in the hierarchy is
                       checked and populated if there are any holes.
        :type logger: BurinLogger
        """

        name = logger.name
        sepIndex = name.rfind(".")
        parent = None

        while sepIndex > 0 and parent is None:
            subName = name[:sepIndex]

            if subName not in self.loggerDict:
                # Create a placeholder if there is no parent already
                self.loggerDict[subName] = _BurinPlaceholder(logger)
            else:
                potentialParent = self.loggerDict[subName]

                if isinstance(potentialParent, BurinLogger):
                    parent = potentialParent
                else:
                    # If not a logger it should be a placeholder
                    potentialParent.append(logger)

            sepIndex = name.rfind(".", 0, sepIndex - 1)

        if not parent:
            parent = self.root

        logger.parent = parent

    def _fixup_children(self, placeHolder, logger):
        """
        Ensures that the children of a placeholder is moved to the logger.

        When a placeholder in the hierarchy is replaced with a logger all of
        that placeholder's children must be moved to the logger so it can take
        the place in the hierarchy.

        :param placeholder: The placeholder being replaced in the hierarchy.
        :type placeholder: _BurinPlaceholder
        :param logger: The new logger replacing the placeholder.
        :type logger: BurinLogger
        """

        name = logger.name
        nameLength = len(name)

        for child in placeHolder.loggerMap.keys():
            if child.parent.name[:nameLength] != name:
                logger.parent = child.parent
                child.parent = logger

    def _clear_cache(self):
        """
        Clears the call of all loggers.

        This is called when level changes are made as the cache of each logger
        will need to be rebuilt to ensure it is accurate.
        """

        with _BurinLock:
            for logger in self.loggerDict.values():
                if isinstance(logger, BurinLogger):
                    logger._cache.clear()

            self.root._cache.clear()

    # Aliases for better compatibility to replace standard library logging
    getLogger = get_logger
