"""
Burin Handlers References

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python Imports
import weakref

# Burin Imports
from .._threading import _BurinLock


_handlers = weakref.WeakValueDictionary()
_handlerList = []


def _add_handler_ref(handler):
    """
    Adds a handler to the internal cleanup list.

    :param handler: The handler to add to the interal reference list.
    :type handler: BurinHandler
    """

    with _BurinLock:
        _handlerList.append(weakref.ref(handler, _remove_handler_ref))

def _remove_handler_ref(handler):
    """
    Removes a handler reference from the internal cleanup list.

    This is normally just called during shutdown as part of the handler
    cleanup.

    :param handler: The handler to remove from the internal reference list.
    :type handler: BurinHandler
    """

    # Pre-emptively grab values which may be cleared during teardown/shutdown
    # and cause failures if not checked.
    lock = _BurinLock
    handlerList = _handlerList

    if lock and handlerList:
        with lock:
            try:
                handlerList.remove(handler)
            except ValueError:
                pass
