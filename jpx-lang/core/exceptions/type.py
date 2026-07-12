"""core/exceptions/type.py - Type errors."""
from .base import JPXError


class JPXTypeError(JPXError):
    """Type mismatch error (e.g., adding string to int)."""
    pass
