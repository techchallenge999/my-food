import logging


class DomainException(Exception):
    def __init__(self, message: str):
        self.logger: logging.Logger = logging.getLogger("DomainException")
        self.message = message
        super().__init__(message)


class UnavailableUUIDException(DomainException):
    def __init__(self, message="Unavailable UUID."):
        super().__init__(message)


class InvalidUUIDException(DomainException):
    def __init__(self, message="Invalid UUID."):
        super().__init__(message)
