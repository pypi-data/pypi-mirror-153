.. currentmodule:: burin

================
The Burin Module
================

.. contents:: Module Contents
    :backlinks: none
    :depth: 2
    :local:


--------
Overview
--------

.. module:: burin
    :synopsis: Logging with added features and convenience.

Within Burin everything needed for normal usage is available on the top-level
``burin`` module.  There is typically no need to import any other packages or
modules from within Burin.

Formatters, loggers, and handlers are all documented in their own sections.
This page will focus on the :ref:`burin:Constants`, :ref:`burin:Attributes`,
and :ref:`burin:Functions` that are available directly on the ``burin`` module.

---------
Constants
---------

The logging levels are integer values that correspond to a kind of seriousness
of a logging event; with higher values being more serious.

Whenever you need to pass a logging level these values can be used directly
such as ``burin.DEBUG``, as string representations like ``"DEBUG"``, or as
straight integer values.

.. note::

    Burin does not currently support customisation or adding of your own log
    levels.  This is planned to be added in a future release.

.. data:: CRITICAL
    :value: 50

.. data:: ERROR
    :value: 40

.. data:: WARNING
    :value: 30

.. data:: INFO
    :value: 20

.. data:: DEBUG
    :value: 10

.. data:: NOTSET
    :value: 0

----------
Attributes
----------

There are a handful of attributes on the Burin module that control some aspects
of logging.  Most of these control whether some data is available for inclusion
in logs or not.

.. data:: logMultiprocessing
    :value: True

    Whether multiprocessing details should be available for inclusion in logs.

.. data:: logProcesses
    :value: True

    Whether process details should be available for inclusion in logs.

.. data:: logThreads
    :value: True

    Whether threading details should be available for inclusion in logs.

.. data:: raiseExceptions
    :value: True

    Used to set if exceptions during handling should be propagated or ignored.

---------
Functions
---------

There are many top-level functions within the Burin module.  These provide ways
to configure logging, get loggers, log directly, or add customised
functionality.

.. note::

    Many of these functions will have slight changes from the standard
    :mod:`logging` module due to added functionality.

    In most use cases though calling any of these functions in the same way as
    the :mod:`logging` module should work exactly the same way.

.. note::

    All of the functions with an *underscore_separated* name also have a
    *camelCase* alias name which matches the names used in the standard
    :mod:`logging` library.

Below is a summary list of all functions in the module; and then further below
are the full details of the functions grouped into categories based on their
general purpose.

.. autosummary::
    :nosignatures:

    basic_config
    capture_warnings
    critical
    debug
    disable
    error
    exception
    get_level_name
    get_log_record_factory
    get_logger
    get_logger_class
    info
    log
    make_log_record
    set_log_record_factory
    set_logger_class
    shutdown
    warning

~~~~~~~~~~~~~
Configuration
~~~~~~~~~~~~~

These functions are used to configure the logging setup.

.. note::

    Burin does not yet support functionality similar to the
    :mod:`logging.config` ``dictConfig``, ``fileConfig``, and ``listen``
    functions.  This is planned to be added in a future release.

.. autofunction:: basic_config

~~~~~~~
Logging
~~~~~~~

These functions can be used directly to log messages with either the root
logger or another logger by using the *logger* parameter to specify the name.

.. autofunction:: critical

.. autofunction:: debug

.. autofunction:: error

.. autofunction:: exception

.. autofunction:: info

.. autofunction:: log

.. autofunction:: warning

~~~~~~~
Loggers
~~~~~~~

These are the top-level functions you can use to get logger instances or to
customise the logger class used.

.. autofunction:: get_logger

.. autofunction:: get_logger_class

.. autofunction:: set_logger_class

~~~~~~~~~~~
Log Records
~~~~~~~~~~~

The log record classes are used to represent the log event values and format
the passed log message before output.  These are referred to as factories when
logger instances create an instance of the record for an event.

The built-in log record factories provide different formatting options as
demonstrated in :ref:`intro:Deferred Formatting Styles`.  However custom log
record factories can also be added by using the :func:`set_log_record_factory`.
An example of this is shown in :ref:`intro:Customisable Log Records`.

.. autofunction:: get_log_record_factory

.. autofunction:: make_log_record

.. autofunction:: set_log_record_factory

~~~~~~~~~~
Log Levels
~~~~~~~~~~

These functions are meant to help with some situations dealing with logging
levels.  For example disabling all logging of specific levels with one
simple call, and providing a helper method that may be useful for some
wrappers.

.. note::

    Burin does not currently support customisation or adding of your own log
    levels.  This is planned to be added in a future release.

.. autofunction:: disable

.. autofunction:: get_level_name

~~~~~~~~~~~~~~~~~~~~
Warnings Integration
~~~~~~~~~~~~~~~~~~~~

Like the Python standard :mod:`logging` package Burin also supports some
integration with the :mod:`warnings` module.

.. autofunction:: capture_warnings

~~~~~~~~
Clean Up
~~~~~~~~

Burin will handle cleaning up of all handlers automatically when the program
exits, so there shouldn't be any need for manual cleanup. However; if you want
Burin to clean up handlers before then you can call the :func:`shutdown`
function.

.. autofunction:: shutdown
