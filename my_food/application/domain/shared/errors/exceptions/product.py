from my_food.application.domain.shared.errors.handling import DomainException


class InvalidProductQuantityException(DomainException):
    def __init__(self, message='Invalid product quantity.'):
        super().__init__(message)


class UnavailableProductException(DomainException):
    def __init__(self, message='Unavailable product.'):
        super().__init__(message)