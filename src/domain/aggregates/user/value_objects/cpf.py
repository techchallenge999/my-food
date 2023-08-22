from src.domain.aggregates.user.interfaces.value_objects import CpfInterface
from src.domain.aggregates.user.validators.cpf_validator import CpfValidator
from src.domain.shared.interfaces.validator import ValidatorInterface


class Cpf(CpfInterface):
    def __init__(self, value: str):
        self.value = value
        self._validator = CpfValidator(self)
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
