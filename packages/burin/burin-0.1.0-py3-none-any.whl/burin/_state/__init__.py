"""
Burin State Options and Parameters

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import inspect
import os
import time


#: Whether multiprocessing details should be available for inclusion in logs
logMultiprocessing = True

#: Wheter process details should be available for inclusion in logs
logProcesses = True

#: Whether threading details should be available for inclusion in logs
logThreads = True

#: Used to set if exceptions during handling should be propagated or ignored
raiseExceptions = True

# Base for calculating the relative time of events
_internals = {
    "srcDir": None,
    "startTime": time.time()
}


# Setup local references to imports that aren't part of this package
__inspect = inspect
__osPath = os.path
def _set_src_dir(obj):
    """
    Sets the internal source directory of the library.

    This should be called only with an object in a module in the main Burin
    root directory.

    The :attr:`_internals` *srcDir* value can then be checked when walking
    through stack frames to determine when a frame is outside of Burin.

    :param obj: A class, function, attribute, or other object that
                :func:`inspect.getfile` can use to get the source path.
    :type obc: Any
    """

    _internals["srcDir"] = __osPath.dirname(__osPath.normcase(__inspect.getfile(obj)))


__all__ = ["logMultiprocessing", "logProcesses", "logThreads",
           "raiseExceptions"]


# Clean up some things that aren't part of this package
del inspect
del os
del time
