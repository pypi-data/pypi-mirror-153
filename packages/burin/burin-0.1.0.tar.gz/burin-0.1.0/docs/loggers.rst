.. currentmodule:: burin

===========================
Loggers and Logger Adapters
===========================

:class:`BurinLogger` instances are what actually handle and process logging
events.  Each logger will have a unique name and can have its own handlers,
formatters, and message style.

Loggers also exist in a hierarchy, by default loggers will propagate their
logging events up through the hierarchy so handlers assigned to other loggers
higher up will also receive the event.  This simplifies things as handlers
don't need to be set on every single logger.

:class:`BurinLoggerAdapter` instances allow you to predefine *extra* fields and
values for a logger without needing to provide them in every logging call.
This can be useful if you want to log an extra field every time.  Also unlike
the :class:`logging.LoggerAdapter` any *extra* values that are passed in a call
to the adapter will get merged with the defaults that were set; this mean you
can also nest adapters if needed.

.. note::

    All methods of the :class:`BurinLogger` and :class:`BurinLoggerAdapter`
    classes with an *underscore_separated* name also have a *camelCase* alias
    name which matches the names used in the standard :mod:`logging` library.

-----------
BurinLogger
-----------

Most of the methods on a logger are only called internally by other parts of
Burin and do not need to be called directly.  The most commonly used methods
would be :meth:`BurinLogger.add_handler`, :meth:`BurinLogger.critical`,
:meth:`BurinLogger.debug`, :meth:`BurinLogger.error`,
:meth:`BurinLogger.exception`, :meth:`BurinLogger.info`,
:meth:`BurinLogger.log`, and :meth:`BurinLogger.warning`.

Here is a summary list of the methods for the :class:`BurinLogger` class; below
that is a full description of the class, it attributes, and methods.

.. autosummary::
    :nosignatures:

    BurinLogger.add_handler
    BurinLogger.call_handlers
    BurinLogger.critical
    BurinLogger.debug
    BurinLogger.error
    BurinLogger.exception
    BurinLogger.find_caller
    BurinLogger.get_child
    BurinLogger.get_effective_level
    BurinLogger.handle
    BurinLogger.has_handlers
    BurinLogger.info
    BurinLogger.is_enabled_for
    BurinLogger.log
    BurinLogger.make_record
    BurinLogger.remove_handler
    BurinLogger.set_level
    BurinLogger.warning

.. autoclass:: BurinLogger
    :members: add_handler, call_handlers, critical, debug, error, exception,
              find_caller, get_child, get_effective_level, handle,
              has_handlers, info, is_enabled_for, log, make_record,
              remove_handler, set_level, warning

    .. autoproperty:: msgStyle

    .. attribute:: propagate
        :value: True

        Whether logging events should be propagated up the logger hierarchy.

------------------
BurinLoggerAdapter
------------------

Almost all of the methods of the logger adapter mirror the underlying logger or
simply delegate directly to it.  The only unique method to the adapter is
:meth:`BurinLoggerAdapter.process` which is called automatically when a log
call is made.  This can be overridden though to customise an adapter.

.. autoclass:: BurinLoggerAdapter
    :members: critical, debug, error, exception, get_effective_level,
              has_handlers, info, is_enabled_for, log, process, set_level,
              warning

    .. autoproperty:: msgStyle
