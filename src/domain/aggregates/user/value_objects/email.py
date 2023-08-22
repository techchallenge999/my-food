from src.domain.aggregates.user.interfaces.value_objects import EmailInterface
from src.domain.aggregates.user.validators.email_validator import EmailValidator
from src.domain.shared.interfaces.validator import ValidatorInterface


class Email(EmailInterface):
    def __init__(self, value: str):
        self.value = value
        self._validator = EmailValidator(self)
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
