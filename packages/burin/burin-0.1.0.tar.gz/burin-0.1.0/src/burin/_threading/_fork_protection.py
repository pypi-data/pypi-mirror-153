"""
Burin Fork Protection

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python Imports
import os
import weakref

# Burin Imports
from ._lock import _BurinLock


# Adds some protections (when available) for handlers which can have issues
# after forking in some situations (Python issue #36533).
if not hasattr(os, "register_at_fork"):
    # register_at_fork is Unix only and 3.7+ only, if not found do nothing
    def _register_at_fork_reinit_lock(instance):
        """
        This is a stub class that does nothing.

        :func:`os.register_at_fork` is required for this fork protection to
        work, but it is only available on Unix systems with Python 3.7+.
        """
        pass
else:
    # Handlers have a _at_fork_reinit method which is called after
    # forking; a weakref avoids keeping discarded instances alive
    _at_fork_reinit_lock_weakset = weakref.WeakSet()

    def _register_at_fork_reinit_lock(instance):
        """
        This will register a handler to reinitialize its lock after a fork.

        :param instance: The handler instance to register.
        :type instance: BurinHandler
        """

        with _BurinLock:
            _at_fork_reinit_lock_weakset.add(instance)

    def _after_at_fork_child_reinit_locks():
        """
        Reinitializes the locks in handlers after forking.
        """

        for handler in _at_fork_reinit_lock_weakset:
            handler._at_fork_reinit()

        # Parent acquired the lock before forking; this reinitializes it if
        # the method is available (3.9+ in certain conditions)
        try:
            _BurinLock._at_fork_reinit()
        except AttributeError:
            pass

    os.register_at_fork(before=_BurinLock.acquire,
                        after_in_child=_after_at_fork_child_reinit_locks,
                        after_in_parent=_BurinLock.release)
