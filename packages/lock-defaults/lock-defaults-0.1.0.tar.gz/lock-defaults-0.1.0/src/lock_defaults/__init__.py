"""
Function to reset mutable defaults each time the function is called

If in python 3.10 or later uses a different version that works better
with static typing.

Import lockmutabledefault or the alias lockdefaults

"""
__version__ = "0.1.0"

import sys

if sys.version_info >= (3, 10):
    from .with_paramspec.lock_defaults import lockmutabledefaults
else:
    from .without_paramspec.lock_defaults import lockmutabledefaults
