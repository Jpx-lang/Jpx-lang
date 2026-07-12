# exceptions.py - JPX Exception Classes
# Version: 3.0.0
#
# Sebelumnya semua exception classes didefinisikan di sini. Sekarang
# mereka dipindah ke `core/exceptions/` sebagai package modular.
# File ini tetap ada untuk backward compatibility — semua code yang
# import `from .exceptions import JPXSyntaxError` akan tetap jalan.

# Import dari struktur modular baru
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.exceptions import (
    JPXError,
    JPXSyntaxError,
    JPXNameError,
    JPXImportError,
    JPXTypeError,
    JPXAttributeError,
    JPXRuntimeError,
    JPXBreakException,
    JPXContinueException,
    JPXReturnException,
    JPXExceptionWrapper,
)

__all__ = [
    'JPXError',
    'JPXSyntaxError',
    'JPXNameError',
    'JPXImportError',
    'JPXTypeError',
    'JPXAttributeError',
    'JPXRuntimeError',
    'JPXBreakException',
    'JPXContinueException',
    'JPXReturnException',
    'JPXExceptionWrapper',
]
