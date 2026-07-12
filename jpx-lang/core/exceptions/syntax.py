"""core/exceptions/syntax.py - Syntax errors."""
from .base import JPXError


class JPXSyntaxError(JPXError):
    """Syntax error in JPX code (e.g., malformed expression, missing brace)."""
    pass
