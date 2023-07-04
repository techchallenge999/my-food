from my_food.application.domain.shared.errors.handling import DomainException


class InvalidCPFException(DomainException):
    def __init__(self, message='Invalid CPF.'):
        super().__init__(message)


class UnavailableCPFException(DomainException):
    def __init__(self, message='Unavailable CPF.'):
        super().__init__(message)


class InvalidEmailException(DomainException):
    def __init__(self, message='Invalid email.'):
        super().__init__(message)


class InvalidPasswordException(DomainException):
    def __init__(self, message='Invalid password.'):
        super().__init__(message)


class UserNotFoundException(DomainException):
    def __init__(self, message='User not found.'):
        super().__init__(message)
