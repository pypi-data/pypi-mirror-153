__all__ = ["SerializationError", "DeserializationError", "FatalError"]


class SerializationError(Exception):
    """
    Exception raised when
    serialization fails.
    """


class DeserializationError(Exception):
    """
    Exception raised when
    deserialization fails.
    """


class FatalError(Exception):
    """
    General purpose exception.
    """
