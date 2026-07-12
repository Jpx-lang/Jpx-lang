"""core/exceptions/base.py - Base exception classes for JPX."""


class JPXError(Exception):
    """Base exception for all JPX errors."""
    pass


class JPXExceptionWrapper(Exception):
    """Wrapper untuk semua exception di try-catch.
    Memungkinkan catch block menerima info type dan message dari exception
    yang dilempar."""
    def __init__(self, original_exception):
        self.original = original_exception
        self.message = str(original_exception)
        self.type = type(original_exception).__name__
        super().__init__(self.message)
