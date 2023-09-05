from src.domain.aggregates.user.interfaces.value_objects import PasswordInterface
from src.domain.aggregates.user.validators.password import PasswordValidator


class Password(PasswordInterface):
    def __init__(self, value: str):
        self.value = value
        self._validator = PasswordValidator(self)
        self.validator.validate()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def validator(self):
        return self._validator
