"""
Burin NT Event Log Handler

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2022 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2021 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import NTEventLogHandler
import os.path

# Burin imports
from .._log_levels import CRITICAL, DEBUG, ERROR, INFO, WARNING
from .handler import BurinHandler


class BurinNTEventLogHandler(BurinHandler, NTEventLogHandler):
    """
    A handler which sends events to Windows NT Event Log.

    .. note::

        This is a subclass of :class:`logging.handlers.NTEventLogHandler` and
        functions identically to it in normal use cases.

    To use this handler you must be on a Windows system and have the `pywin32`
    package installed.
    """

    def __init__(self, appname, dllname=None, logtype="Application"):
        """
        This sets the application name and allows using a specific dll.

        During initialization this will try to import the
        :mod:`win32evtlogutil` and :mod:`win32evtlog` modules from the
        `pywin32` package.  If this fails it will print a message to `stdout`
        and the handler that is created will not log anything.

        A registry entry for the *appname* will be created.  Also if *dllname*
        is **None** then *win32service.pyd* is used.  This can cause the
        resulting event logs to be quite large, so you can specify a different
        *dllname* with the message definitions you want to use.

        :param appname: The name of the application which will be added to the
                        registry.
        :type appname: str
        :param dllname: Specify a dll to use other than *win32service.pyd*.
        :type dllname: str
        :param logtype: The log type used to register the event logs.
        :type logtype: str
        """

        BurinHandler.__init__(self)

        try:
            import win32evtlogutil
            import win32evtlog

            self.appname = appname
            self._welu = win32evtlogutil

            if not dllname:
                dllname = os.path.split(self._welu.__file__)
                dllname = os.path.split(dllname[0])
                dllname = os.path.split(dllname[0], r"win32service.pyd")

            self.dllname = dllname
            self.logtype = logtype

            self._welu.AddSourceToRegistry(appname, dllname, logtype)

            self.deftype = win32evtlog.EVENTLOG_ERROR_TYPE
            self.typemap = {
                DEBUG: win32evtlog.EVENTLOG_INFORMATION_TYPE,
                INFO: win32evtlog.EVENTLOG_INFORMATION_TYPE,
                WARNING: win32evtlog.EVENTLOG_WARNING_TYPE,
                ERROR: win32evtlog.EVENTLOG_ERROR_TYPE,
                CRITICAL: win32evtlog.EVENTLOG_ERROR_TYPE
            }
        except ImportError:
            print("The Python Win32 extensions for NT (service and event "
                  "logging) appear to be unavailable")
            self._welu = None

    # Alias methods from the standard library handler
    get_event_category = NTEventLogHandler.getEventCategory
    get_event_type = NTEventLogHandler.getEventType
    get_message_id = NTEventLogHandler.getMessageID

    def close(self):
        """
        Closes the handler.
        """

        BurinHandler.close(self)
