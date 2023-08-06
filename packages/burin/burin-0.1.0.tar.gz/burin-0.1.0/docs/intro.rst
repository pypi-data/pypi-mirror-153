.. currentmodule:: burin

==========================
What's Different in Burin?
==========================

The following make up the current major differences compared to the Python
standard :mod:`logging` module.

* Extra arguments and changes to :func:`basic_config` allow it to be used in
  more situations and when setting up common logging configurations.
* Built-in support for deferred formatting of :meth:`str.format` and
  :class:`string.Template` style logging messages.
* Library level logging calls (eg. :func:`burin.log`) can specify a logger to
  use other than the root logger, so calling :func:`get_logger` isn't necessary
  first.
* Logging features from newer versions of Python (eg.
  :class:`logging.Formatter` *defaults* in 3.10) are implemented in Burin and
  available in all supported Python versions.
* Everything that should be needed is available at the top level of the
  library; no more extra imports of :mod:`logging.handlers` and
  :mod:`logging.config`.
* Multiple log record factory classes are supported at the same time, and which
  is used can be set per logger instance to allow for greater customisation.
* :class:`BurinLoggerAdapter` instances will merge *extra* values from logging
  calls with the pre-set values from instantiation; nesting built-in adapters
  is actually useful.
* :class:`BurinSocketHandler` and :class:`BurinDatagramHandler` by default use
  pickling protocol version **4** instead of **1**.  This can be set to a
  different protocol version when creating the handler.
* All methods and functions are *underscore_separated*, but *camelCase* aliases
  are available for an easier transition from the standard library.
* Deprecated methods such as ``fatal`` and ``warn`` are not implemented.

There are several minor differences which are internal to Burin and not
documented here.  Just be sure to read the documentation if you are going to
create subclasses, or read the docstrings in the code if accessing internal
classes and methods.

====================
What Can't Burin Do?
====================

Burin is still in early development and does not yet support some use cases
that are supported by Python :mod:`logging`.  These features are planned to
be implemented before Burin reaches its first stable major (1.0.0) release.

* Advanced configuration functions like those from :mod:`logging.config`
  (``dictConfig``, ``fileConfig``, and ``listen``) are not yet implemented.
* Custom log levels are not yet supported.

===========
Using Burin
===========

Below are a few examples of using the features of Burin.  Read through the rest
of the documentation to see the full information on the functionality of Burin.

.. note::

    All Burin functions and methods are *underscore_separated*, however to ease
    changing from the standard library they all also have *camelCase* aliases.

    Throughout this documentation the *underscore_separated* names are used,
    but every time you see a function or method call in Burin just remember
    that the *camelCase* name (like what is in :mod:`logging`) will also work.

Burin can be imported and used similar to the :mod:`logging` standard library
package.

.. code-block:: python

    import burin
    burin.basic_config()
    logger = burin.get_logger()
    logger.info("I am a log message.")

What is above would do the exact same thing with both Burin and :mod:`logging`.

-----------------------
A Not So "Basic" Config
-----------------------

However compared to the standard :mod:`logging` package; using Burin can be
much simpler for certain things, or even allow some functionality that would
otherwise require custom wrapper utilities or overriding logging subclasses.

For example a common logging setup may be to output info level logs to a
rotating file with a specific format, and also output warning level logs to
``sys.stderr`` in a different format.

With Burin setting this up can be accomplished with 2 imports and 1 call to
:func:`basic_config`.

.. code-block:: python

    import sys
    import burin
    burin.basic_config(filename="prog.log", filelevel="INFO", filerotate=True,
                       fileformat="{asctime} - {levelname} :{name}: {message}",
                       filerotatesize=1048576, filerotatecount=9, level="INFO",
                       stream=sys.stderr, streamlevel="WARNING",
                       streamformat="{levelname}: {message}", style="{")

Whereas with :mod:`logging` this takes 3 imports and 12 lines.

.. code-block:: python

    import sys
    import logging
    from logging.handlers import RotatingFileHandler
    fileForm = logging.Formatter("{asctime} - {levelname} :{name}: {message}",
                                 style="{")
    fileHand = RotatingFileHandler("prog.log", maxBytes=1048576, backupCount=9)
    fileHand.setFormatter(fileForm)
    fileHand.setLevel("INFO")
    streamForm = logging.Formatter("{levelname}: {message}", style="{")
    streamHand = logging.StreamHandler(sys.stderr)
    streamHand.setFormatter(streamForm)
    streamHand.setLevel("WARNING")
    rootLogger = logging.getLogger()
    rootLogger.addHandler(fileHand)
    rootLogger.addHandler(streamHand)
    rootLogger.setLevel("INFO")

--------------------------
Deferred Formatting Styles
--------------------------

Burin also supports deferred formatting with log messages using
:meth:`str.format` and :class:`string.Template` style strings, as well as the
'%' style formatting that the standard library does.  Which formatting is used
is set by the :attr:`BurinLogger.msgStyle` property on a logger which can also
be specified when calling :func:`get_logger`.

.. code-block:: python

    formatLogger = burin.get_logger("formatLogger", "{")
    formatLogger.debug("This is a {} event in {}", "DEBUG", "Burin")
    templateLogger = burin.get_logger("templateLogger", msgStyle="$")
    templateLogger.debug("This is a ${lvl} event in ${prog}", lvl="DEBUG",
                         prog="Burin")

Setting this on the root logger will set the default style for new loggers as
well.

.. code-block:: python

    rootLogger = burin.get_logger(msgStyle="{")
    newLogger = burin.get_logger("new")
    newLogger.debug("This is a {lvl} event in {prog}", lvl="DEBUG",
                    prog="Burin")

Deferred formatting means that all of the extra formatting is only done if a
message will be logged, so this can be more efficient than doing the formatting
on the string beforehand.

For a bit more information about the deferred logging see
:meth:`BurinLogger.log`.

------------------------
Customisable Log Records
------------------------

Setting the :attr:`msgStyle` of a logger actually sets the log record factory
that is used.  While the default built-in factories are focused on formatting,
you can actually add any other custom factories that may be useful in your
program. These factories can then just be used where needed instead of for all
log messages as in the standard library.

This can be incredibly useful when you need a log to display values in a
specific way, but only want that extra processing to run if the log
message will actually be output.

To add your own factory simply create a subclass of :class:`BurinLogRecord` and
then set it to a *msgStyle* with :func:`set_log_record_factory`.

.. code-block:: python

    class HexRecord(burin.BurinLogRecord):
        """
        Converts all int argument values to hex strings for log output.
        """

        def get_message(self):
            msg = str(self.msg)
            if self.args or self.kwargs:
                hexArgs = []
                hexKwargs = {}

                for eachArg in self.args:
                    if isinstance(eachArg, int):
                        eachArg = hex(eachArg)
                    hexArgs.append(eachArg)

                for eachKey, eachValue in self.kwargs.items():
                    if isinstance(eachValue, int):
                        eachValue = hex(eachValue)
                    hexKwargs[eachKey] = eachValue

                msg = msg.format(*hexArgs, **hexKwargs)
            return msg

    burin.set_log_record_factory(HexRecord, "hex")

In this example you would now be able to use ``hex`` as a *msgStyle* for any
loggers where you want int *args* and *kwargs* converted to a hexadecimal
string when the log message is output.
