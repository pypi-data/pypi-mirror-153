.. currentmodule:: burin

==========
Formatters
==========

The purpose of a formatter is to convert a :class:`BurinLogRecord` into
(typically) a textual representation of the logging event according to a
specified format.

A :class:`BurinFormatter` should be set on every handler, but if a handler
doesn't have one then a very simple formatter will be used instead.

If multiple logs need to be formatted in a batch for a custom handler then a
:class:`BurinBufferingFormatter` can be used or a subclass of it can be created
to meet those needs.

--------------
BurinFormatter
--------------

The :class:`BurinFormatter` is derived from :class:`logging.Formatter` and
should function identically in almost all use cases.


.. note::

    All methods of the :class:`BurinFormatter` with an *underscore_separated*
    name also have a *camelCase* alias name which matches the names used in the
    standard :mod:`logging` library.

.. autoclass:: BurinFormatter
    :members: format, format_time

-----------------------
BurinBufferingFormatter
-----------------------

This cannot be used by any built-in handlers but provides a class that can be
used for formatting a batch of log records at once if needed by a custom
handler.

.. autoclass:: BurinBufferingFormatter
