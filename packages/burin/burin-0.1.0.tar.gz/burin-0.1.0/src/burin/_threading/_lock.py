"""
Burin Lock

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python Imports
from threading import RLock

#: A reentrant lock used within Burin to protect some shared resources.
_BurinLock = RLock()
