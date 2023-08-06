"""
Burin Exceptions

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

class ConfigError(Exception):
    """
    General exception for configuration errors.
    """
    pass


class FactoryError(Exception):
    """
    General exception for errors setting or using log record factories.
    """
    pass


class FormatError(Exception):
    """
    General exception for formatting errors.
    """
    pass


__all__ = ["ConfigError", "FactoryError", "FormatError"]
