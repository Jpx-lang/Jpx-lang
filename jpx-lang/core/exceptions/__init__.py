"""
core/exceptions/__init__.py - JPX Exception module (package)

Re-exports semua exception classes dari sub-modules. Memungkinkan import
seperti:
    from core.exceptions import JPXSyntaxError
atau
    from core.exceptions.syntax import JPXSyntaxError

Struktur sebagai package memungkinkan organisasi exception yang lebih
modular saat jumlahnya bertambah di masa depan.
"""

from .base import (
    JPXError,
    JPXExceptionWrapper,
)
from .syntax import JPXSyntaxError
from .name import JPXNameError
from .type import JPXTypeError
from .attribute import JPXAttributeError
from .runtime import JPXRuntimeError, JPXImportError
from .control import (
    JPXBreakException,
    JPXContinueException,
    JPXReturnException,
)

__all__ = [
    'JPXError',
    'JPXExceptionWrapper',
    'JPXSyntaxError',
    'JPXNameError',
    'JPXTypeError',
    'JPXAttributeError',
    'JPXRuntimeError',
    'JPXImportError',
    'JPXBreakException',
    'JPXContinueException',
    'JPXReturnException',
]
