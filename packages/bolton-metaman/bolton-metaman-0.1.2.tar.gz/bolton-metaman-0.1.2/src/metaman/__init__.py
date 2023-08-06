"""metaman package

metadata manager (METAMAN)... Makes use of Python's dynamic nature to inspect a
program's internals.
"""

import logging as _logging

from ._core import Inspector, cname, register_function_factory, scriptname
from ._deprecate import MetamanDeprecationWarning, deprecated


__all__ = [
    "Inspector",
    "MetamanDeprecationWarning",
    "deprecated",
    "cname",
    "register_function_factory",
    "scriptname",
]

__author__ = "Bryan M Bugyi"
__email__ = "bryanbugyi34@gmail.com"
__version__ = "0.1.2"

_logging.getLogger(__name__).addHandler(_logging.NullHandler())
