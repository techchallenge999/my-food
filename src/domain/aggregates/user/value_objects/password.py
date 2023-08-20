from src.domain.aggregates.user.interfaces.value_objects import PasswordInterface
from src.domain.aggregates.user.validators.password_validator import PasswordValidator
from src.domain.shared.interfaces.validator import ValidatorInterface


class Password(PasswordInterface):
    def __init__(self, value: str):
        self.value = value
        self._validator = PasswordValidator(self)
        self.validator.validate()

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator
