"""core/exceptions/runtime.py - Runtime errors."""
from .base import JPXError


class JPXRuntimeError(JPXError):
    """Generic runtime error."""
    pass


class JPXImportError(JPXError):
    """Module import error (e.g., module not found, circular import)."""
    pass
