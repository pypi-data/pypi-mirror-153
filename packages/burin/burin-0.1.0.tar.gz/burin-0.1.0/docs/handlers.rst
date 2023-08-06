.. currentmodule:: burin

========
Handlers
========

Handlers are responsible for emitting the log record to specific destination.
All handlers within Burin are derived from the :class:`BurinHandler` class.

.. note::

    Even though many handlers in Burin inherit from handlers within the
    standard :mod:`logging` package, they cannot be used interchangeably.

    Using :mod:`logging` handlers with Burin or Burin handlers with
    :mod:`logging` will cause issues and may result in exceptions or lost logs.

.. note::

    Only methods defined within each Burin handler class are documented here.
    All handlers inherit from the :class:`BurinHandler` class and will also
    mention in their description if they inherit from any other handlers.

    If a handler inherits from the :mod:`logging` package then methods that
    have not been changed are not documented here.

    Additionally all methods of handler classes with an *underscore_separated*
    name also have a *camelCase* alias name which matches the names used in the
    standard :mod:`logging` library.

Below is a list of all handlers available within Burin.  After that detailed
descriptions of each handler is provided.

.. autosummary::
    :nosignatures:

    BurinBaseRotatingHandler
    BurinBufferingHandler
    BurinDatagramHandler
    BurinFileHandler
    BurinHandler
    BurinHTTPHandler
    BurinMemoryHandler
    BurinNTEventLogHandler
    BurinNullHandler
    BurinQueueHandler
    BurinQueueListener
    BurinRotatingFileHandler
    BurinSMTPHandler
    BurinSocketHandler
    BurinStreamHandler
    BurinSyslogHandler
    BurinTimedRotatingFileHandler
    BurinWatchedFileHandler

------------------------
BurinBaseRotatingHandler
------------------------

This is the base rotating handler which can be used by any handlers that need
to rotate files.  This should not be used directly but instead can be inherited
from to create custom handlers.

.. autoclass:: BurinBaseRotatingHandler
    :members: do_rollover, emit, should_rollover

---------------------
BurinBufferingHandler
---------------------

This is a base buffering handler which can be used to create other handlers
which requiring a buffering pattern.  This should not be used directly but
instead can be inherited from to create custom handlers.

.. autoclass:: BurinBufferingHandler
    :members: close

--------------------
BurinDatagramHandler
--------------------

This handler can be used to send logs through a datagram socket to another
Python application.

.. autoclass:: BurinDatagramHandler
    :members: make_socket, send

----------------
BurinFileHandler
----------------

This handler allows for simply writing logs out to a file.

.. autoclass:: BurinFileHandler
    :members: close, emit

------------
BurinHandler
------------

This is the base handler class that all other handlers in Burin are derived
from.  This should not be used directly but instead can be inherited from to
create custom handlers.

.. autoclass:: BurinHandler
    :members: close, create_lock, format, handle_error, set_level

    .. autoproperty:: name

----------------
BurinHTTPHandler
----------------

This handler can send logs to another service using HTTP.

.. autoclass:: BurinHTTPHandler
    :members: get_connection

------------------
BurinMemoryHandler
------------------

This handler can buffer logs in memory until a specified capacity is reached.

.. autoclass:: BurinMemoryHandler
    :members: close

----------------------
BurinNTEventLogHandler
----------------------

This handler can log to the Windows event log; this requires the `pywin32`
package.

.. autoclass:: BurinNTEventLogHandler
    :members: close

----------------
BurinNullHandler
----------------

This handler doesn't do anything, but can be used to ensure a logger has a
configured handler that doesn't actually output to anything (not even
`sys.stderr`).  This may be useful in libraries where you want to use Burin
if it's available, but want to let the application configure the output
handlers.

.. autoclass:: BurinNullHandler
    :class-doc-from: class
    :members: create_lock, emit, handle

-----------------
BurinQueueHandler
-----------------

This handler adds all logs to a queue which a :class:`BurinQueueListener` can
then process.  This can be useful in a multiprocess application to have one
process handle all of the actual logging (and I/O involved) while the others
just add to the queue.

.. autoclass:: BurinQueueHandler

------------------
BurinQueueListener
------------------

This can be paired with :class:`BurinQueueHandler` to have one process for a
queue of logs which multiple handlers add to.

.. autoclass:: BurinQueueListener
    :class-doc-from: class

------------------------
BurinRotatingFileHandler
------------------------

This handler can automatically rotate a log file when it reaches a specific
size.

.. autoclass:: BurinRotatingFileHandler

----------------
BurinSMTPHandler
----------------

This handler can send logs through email using a SMTP server.

.. autoclass:: BurinSMTPHandler

------------------
BurinSocketHandler
------------------

This handler can send pickled log records through a socket to another Python
application.

.. autoclass:: BurinSocketHandler
    :members: close, handle_error, make_pickle

------------------
BurinStreamHandler
------------------

This handler can write logs to an I/O stream.

.. autoclass:: BurinStreamHandler
    :members: set_stream

------------------
BurinSyslogHandler
------------------

This handler can write logs out using Syslog.

.. autoclass:: BurinSyslogHandler
    :members: close

-----------------------------
BurinTimedRotatingFileHandler
-----------------------------

This handler can rotate log files based on a timing pattern.

.. autoclass:: BurinTimedRotatingFileHandler

-----------------------
BurinWatchedFileHandler
-----------------------

This handler watches the file it is writing to and will close and reopen it
automatically if it detects any changes.

.. autoclass:: BurinWatchedFileHandler
    :members: emit
