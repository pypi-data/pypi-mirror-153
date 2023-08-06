"""
Burin Warnings Capture

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import warnings

# Burin imports
from .._handlers import BurinNullHandler
from .._logging import get_logger


# Local warnings reference for use and to restore when stopping override; this
# is modified when capture is enabled/disabled
_warningsShowwarning = None


def capture_warnings(capture):
    """
    Enables or disables capturing of warnings through logs instead.

    When this is enabled :func:`warnings.showwarning` is overridden with a
    function that will automatically log all warnings that are called through
    :func:`warnings.showwarning`.

    :param capture: Enable or disabled capturing of warnings for log output.
    :type capture: bool
    """

    global _warningsShowwarning

    if capture:
        if _warningsShowwarning is None:
            _warningsShowwarning = warnings.showwarning
            warnings.showwarning = _showarning
    else:
        if _warningsShowwarning is not None:
            warnings.showwarning = _warningsShowwarning
            _warningsShowwarning = None

def _showarning(message, category, filename, lineno, file=None, line=None):
    """
    This is meant to override the :func:`warnings.showwarning`.

    This will output the warnings using a logger; however if *file* is not
    **None** then the normal :func:`warnings.showwarning` is called instead.

    :param message: The warning message which will be logged.
    :type message: str | Warning
    :param category: The type of warning.
    :type category: Warning
    :param filename: The filename where the warning originated.
    :type filename: str
    :param lineno: The line number where the warning originated.
    :type lineno: int
    :param file: The file to write the warnint too.  If this is not **None**
                 then the standard :func:`warnings.showwarning` is called
                 instead.
    :type file: io.StringIO
    :param line: An line of source code to the included in the warning.
    :type line: str
    """

    if file is not None:
        if _warningsShowwarning is not None:
            _warningsShowwarning(message, category, filename, lineno, file,
                                 line)
    else:
        # Get the warning as a string and a logger
        formattedWarning = warnings.formatwarning(message, category, filename,
                                                  lineno, line)
        logger = get_logger("py.warnings")

        # If the logger doesn't have any handlers use a Null handler to prevent
        # an error
        if not logger.has_handlers():
            logger.add_handler(BurinNullHandler())

        logger.warning(formattedWarning)


# Aliases for better compatibility to replace standard library logging
captureWarnings = capture_warnings
