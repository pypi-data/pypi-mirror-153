"""This module contains Exception(s) to help debugging.

Typical usage example:

try:
    ...
except Error:
    raise exceptions.JSONChangedError("Helpful message")

Copyright (c) 2022 JackBorah
MIT License see LICENSE for more details
"""

class JSONChangedError(Exception):
    """Should the structure of a blizzard response change this error will be raised"""
