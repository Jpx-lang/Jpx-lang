"""core/exceptions/control.py - Control flow exceptions.

These exceptions are used internally to implement control flow constructs
like `break`, `continue`, and `return` from within nested function/loop
executions. They should NOT be raised by user code directly.
"""
from .base import JPXError


class JPXBreakException(JPXError):
    """Exception untuk keluar dari loop (break)."""
    pass


class JPXContinueException(JPXError):
    """Exception untuk lanjut ke iterasi berikutnya (continue)."""
    pass


class JPXReturnException(Exception):
    """Exception untuk return dari function. Bukan subclass JPXError karena
    ini adalah control flow, bukan error — tapi tetap perlu ditangkap oleh
    function call handler."""
    def __init__(self, value):
        self.value = value
        super().__init__(f"Return: {value}")
