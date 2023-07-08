from my_food.application.domain.shared.errors.exceptions.base import DomainException


class InvalidOrderStatusException(DomainException):
    def __init__(self, message="Invalid order status."):
        super().__init__(message)


class OrderNotFoundException(DomainException):
    def __init__(self, message="Order not found."):
        super().__init__(message)


class NoOrderFoundException(DomainException):
    def __init__(self, message="No order found."):
        super().__init__(message)
