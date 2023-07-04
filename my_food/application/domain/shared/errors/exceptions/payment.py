from my_food.application.domain.shared.errors.exceptions.base import DomainException


class InvalidPaymentStatusException(DomainException):
    def __init__(self, message="Invalid payment status."):
        super().__init__(message)
