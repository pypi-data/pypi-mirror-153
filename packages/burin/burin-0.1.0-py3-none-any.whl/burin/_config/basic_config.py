"""
Burin Basic Configuration

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Burin imports
from .._exceptions import ConfigError
from .._formatters import BurinFormatter, _styles
from .._handlers import BurinFileHandler, BurinRotatingFileHandler, BurinStreamHandler
from .._logging import logRecordFactories, root
from .._threading import _BurinLock


def basic_config(*, datefmt=None, encoding=None, errors="backslashreplace",
                 filedatefmt=None, fileformat=None, filelevel=None,
                 filemode="a", filename=None, filerotate=False,
                 filerotatecount=4, filerotatesize=1048576, force=False,
                 format=None, handlers=None, level="WARNING", msgstyle="%",
                 stream=None, streamdatefmt=None, streamformat=None,
                 streamlevel=None, style="%"):
    """
    Does a basic configuration of the Burin root logger.

    This function will configure handlers for the root logger.  This is a
    convenience method intended to cover several common logging use cases.

    .. note::

        All arguments to this function are optional and must be passed as
        keyword arguments, no positional arguments are supported.

    With this function a file handler (or rotating file hander) and stream
    handler can both be added to the root logger.  An iterable of other
    *handlers* can also be added.  This differs from the standard
    :func:`logging.basicConfig` where only one of these can be configured.

    The file and stream handlers can each have a different *format*, *datefmt*,
    and *level* using the parameters prefixed with *file* or *stream*.  The
    general *format*, *datefmt*, and *level* parameters are used if file or
    stream specific values are not set.

    Any handler within *handlers* that does not have a formatter will have
    a formatter set for them using the general *format* and *datefmt*.

    If the root logger already has handlers this function can still be used to
    add additional *handlers*, configure new file and/or stream handlers for
    the root logger, and change other settings of the root logger.  This
    differs from the standard :func:`logging.basicConfig` where nothing would
    be done if the root logger already has handlers.

    If *handlers*, *filename*, and *stream* are all **None**, and the root
    logger does not have any handlers then a stream handler using
    :obj:`sys.stderr` is created and added to the root logger.  If these
    arguments are all **None** and the root logger does have handlers then the
    other configuration values are still applied if set (*level* and
    *msgstyle*).

    :param datefmt: The date/time format to use (as accepted by
                    :func:`time.strftime`).
    :type datefmt: str
    :param encoding: If specified with a filename this is passed to the handler
                     and used when the file is opened.
    :type encoding: str
    :param errors: If specified with filename this is passed to the handler and
                   used when the file is opened.  (Default =
                   'backslashreplace')
    :type errors: str
    :param filedatefmt: The date/time format to use specifically for the file
                        handler.  If this is **None** than the general
                        *datefmt* argument is used instead.
    :type filedatefmt: str
    :param fileformat: The format string to use specifically for the file
                       handler.  If this is **None** than the general *format*
                       argument is used instead.
    :type fileformat: str
    :param filelevel: The level to set specifically for the file handler.  If
                      this is **None** then the general *level* argument is
                      used instead.
    :type level: int | str
    :param filemode: If specified with filename then this is the mode with
                     which the file is opened.  (Default = 'a')
    :type filemode: str
    :param filename: Specifies that a file handler is to be created and the
                     file path to write to.
    :type filename: str | pathlib.Path
    :param filerotate: Whether a rotating file handler or normal file handler
                       should be created.  (Default = **False**)
    :type filerotate: bool
    :param filerotatecount: If *filerotate* is **True** then this is how many
                            extra log files should be kept after rotating.
                            (Default = 4)
    :type filerotatecount: int
    :param filerotatesize: If *filerotate* is **True** then this sets the size
                           of the log file in bytes before it should be
                           rotated. (Default = 1048576 (1MB))
    :type filerotatesize: int
    :param force: Whether all existing handlers on the root logger should be
                  removed and closed.  (Default = **False**)
    :type force: bool
    :param format: The format string to use for the handlers.  If this is
                   **None** then a default format string will be used that has
                   the level, logger name, and message.
    :type format: str
    :param handlers: This can be an iterable of handlers that were already
                     created and should be added to the root logger.  Any
                     handler within that doesn't have a formatter will have the
                     general formatter assigned to it.
    :type handlers: list[BurinHandler]
    :param level: The level to set on the root logger.  You can set separate
                  levels for the file and stream handlers by using the
                  *filelevel* and *streamlevel* parameters.  (Default =
                  'WARNING')
    :type level: int | str
    :param msgstyle: This sets the style that is used for deferred formatting
                     of log messages on the root logger.  This will also change
                     the default style for any new loggers created afterwards.
                     Built in possible values are '%' for %-formatting, '{' for
                     :meth:`str.format` formatting, and '$' for
                     :class:`string.Template` formatting.  Other values can be
                     used if custom log record factories are added using
                     :func:`set_log_record_factory`. (Default = '%')
    :type msgstyle: str
    :param stream: Specifies that a stream handler is to be created with the
                   passed stream for output.
    :type stream: io.TextIOBase
    :param streamdatefmt: The date/time format to use specifically for the
                          stream handler.  If this is **None** than the general
                          *datefmt* argument is used instead.
    :type streamdatefmt: str
    :param streamformat: The format string to use specifically for the stream
                         handler.  If this is **None** than the general
                         *format* argument is used instead.
    :type streamformat: str
    :param streamlevel: The level to set specifically for the stream handler.
                        If this is **None** then the general *level* argument
                        is used instead.
    :type streamlevel: int
    :param style: The type of formatting to use for the format strings.
                  Possible values are '%' for %-formatting, '{' for
                  :meth:`str.format` formatting, and '$' for
                  :class:`string.Template` formatting. (Default = '%')
    :type style: str
    :raises ConfigError: If *msgstyle* does not match a type of log record
                         factory.
    :raises FormatError: If there are errors with the *format*, *fileformat*,
                         or *streamformat* strings or *style*.
    """

    with _BurinLock:
        # Ensure a valid msgstyle is used
        if msgstyle not in logRecordFactories:
            raise ConfigError(f"Unknown msgstyle {msgstyle!r}; must be one of: "
                              f"{', '.join(logRecordFactories.keys())}")

        # Use a default format if none is set
        format = format if format is not None else _styles[style]["default"]

        # Get the basic formatter setup
        basicFormatter = BurinFormatter(format, datefmt, style)

        # Remove all existing handlers from the root logger
        if force:
            # Go through a copy of the handlers for the root logger and remove
            # them
            for oldHandler in root.handlers[:]:
                root.remove_handler(oldHandler)
                oldHandler.close()

        # Add any received handlers to the root logger
        if handlers is not None:
            for newHandler in handlers:
                # Give the handler a formatter if it doesn't have one
                if newHandler.formatter is None:
                    newHandler.set_formatter(basicFormatter)

                root.add_handler(newHandler)

        # Setup the file handler if needed
        if filename is not None:
            # Setup the file formatter if needed, otherwise use the basic one
            if fileformat is not None or filedatefmt is not None:
                fileformat = fileformat if fileformat is not None else format
                filedatefmt = filedatefmt if filedatefmt is not None else datefmt
                fileFormatter = BurinFormatter(fileformat, filedatefmt, style)
            else:
                fileFormatter = basicFormatter

            # Create the requested file handler type
            if filerotate:
                fileHandler = BurinRotatingFileHandler(filename, mode=filemode,
                                                       maxBytes=filerotatesize,
                                                       backupCount=filerotatecount,
                                                       encoding=encoding,
                                                       errors=errors)
            else:
                fileHandler = BurinFileHandler(filename, mode=filemode,
                                               encoding=encoding, errors=errors)

            # Set the level on the handler if a specific file level was
            # received
            if filelevel is not None:
                fileHandler.set_level(filelevel)

            # Set the formatter and add the handler to the root logger
            fileHandler.set_formatter(fileFormatter)
            root.add_handler(fileHandler)

        # Setup the stream handler if requested or if no other handlers were
        # set
        if stream is not None or (handlers is None and filename is None and not root.has_handlers()):
            # Setup the stream formatter if needed, otherwise use the basic one
            if streamformat is not None or streamdatefmt is not None:
                streamformat = streamformat if streamformat is not None else format
                streamdatefmt = streamdatefmt if streamdatefmt is not None else datefmt
                streamFormatter = BurinFormatter(streamformat, streamdatefmt,
                                                 style)
            else:
                streamFormatter = basicFormatter

            # Create the stream handler
            streamHandler = BurinStreamHandler(stream)

            # Set the level on the handler if a specific stream level was
            # received
            if streamlevel is not None:
                streamHandler.set_level(streamlevel)

            # Set the formatter and add the handler to the root logger
            streamHandler.set_formatter(streamFormatter)
            root.add_handler(streamHandler)

        # Set the level on the logger if a general level was received
        if level is not None:
            root.set_level(level)

        # Set the msgStyle of the root logger
        root.msgStyle = msgstyle


# Aliases for better compatibility to replace standard library logging
basicConfig = basic_config
