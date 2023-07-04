from my_food.application.domain.shared.errors.handling import DomainException


class InvalidOrderStatusException(DomainException):
    def __init__(self, message='Invalid order status.'):
        super().__init__(message)


class OrderNotFoundException(DomainException):
    def __init__(self, message='Order not found.'):
        super().__init__(message)
