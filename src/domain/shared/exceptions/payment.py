from src.domain.shared.exceptions.base import DomainException


class InvalidPaymentStatusException(DomainException):
    def __init__(self, message="Invalid payment status."):
        super().__init__(message)


class PaymentNotFoundException(DomainException):
    def __init__(self, message="Payment not found."):
        super().__init__(message)
