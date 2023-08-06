"""
Burin Log Levels

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Just duplicated standard library levels for now.
#: Critical logging event level
CRITICAL = 50
#: Error logging event level
ERROR = 40
#: Warning logging event level
WARNING = 30
#: Info logging event level
INFO = 20
#: Debug logging event level
DEBUG = 10
#: Logging event level used for imply an unset level.
NOTSET = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}
_nameToLevel = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}


def get_level_name(level):
    """
    Return the textual or numeric representation of a logging level.

    If a numeric value corresponding to one of the defined levels
    (:const:`CRITICAL`, :const:`ERROR`, :const:`WARNING`, :const:`INFO`,
    :const:`DEBUG`) is passed in, the corresponding string representation is
    returned.

    If a string representation of the level is passed in, the corresponding
    numeric value is returned.

    .. note::

        Unlike the standard library :func:`logging.getLevelName` a lower case
        name can also be used; all level name checks are automatically
        converted to uppercase.

    If no matching numeric or string value is passed in, the string
    ``f'Level {level}'`` level is returned.

    :param level: The logging level to get the text or numeric representation
                  of.
    :type level: int | str
    :returns: If *level* is an *int* then a string representation of the level
              is returned; otherwise, if *level* is a *str* then an integer
              representation of the level is returned.
    :rtype: int | str
    """

    # See Python issues #22386, #27937 and #29220 for why it's this way
    result = _levelToName.get(level)
    if result is not None:
        return result

    if str(level) == level:
        level = level.upper()
        result = _nameToLevel.get(level)
        if result is not None:
            return result
    return f"Level {level}"


# Aliases for better compatibility to replace standard library logging
getLevelName = get_level_name


def _check_level(level):
    """
    Checks if the log level is valid.

    This will always return the numeric representation of *level* if it is
    valid.  If *level* is not valid then it will raise exceptions.

    :param level: The log level to check.
    :type level: int | str
    :returns: The numeric representation of *level*.
    :raises ValueError: If *level* is not a valid logging level.
    :raises TypeError: If *level* is not a string or integer.
    """

    if isinstance(level, int):
        result = level
    elif isinstance(level, str):
        level = level.upper()

        if level not in _nameToLevel:
            raise ValueError(f"Unknown level: {level!r}")
        result = _nameToLevel[level]
    else:
        raise TypeError(f"Level not an integer or a valid string: {level!r}")
    return result


__all__ = ["CRITICAL", "DEBUG", "ERROR", "INFO", "NOTSET", "WARNING",
           "get_level_name", "getLevelName"]
