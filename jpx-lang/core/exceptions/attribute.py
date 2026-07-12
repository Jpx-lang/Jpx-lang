"""core/exceptions/attribute.py - Attribute/property errors."""
from .base import JPXError


class JPXAttributeError(JPXError):
    """Attribute/property not found on object (e.g., accessing missing field
    on a class instance)."""
    pass
