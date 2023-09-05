from src.domain.shared.exceptions.base import DomainException


class InvalidProductQuantityException(DomainException):
    def __init__(self, message="Invalid product quantity."):
        super().__init__(message)


class UnavailableProductException(DomainException):
    def __init__(self, message="Unavailable product."):
        super().__init__(message)


class InvalidProductCategoryException(DomainException):
    def __init__(self, message="Invalid product category."):
        super().__init__(message)


class ProductNotFoundException(DomainException):
    def __init__(self, message="Product not found."):
        super().__init__(message)
