from src.domain.aggregates.user.interfaces.value_objects import CpfInterface
from src.domain.shared.exceptions.user import InvalidCPFException
from src.domain.shared.interfaces.validator import ValidatorInterface


class CpfValidator(ValidatorInterface):
    def __init__(self, entity: CpfInterface):
        self._cpf = entity

    def validate(self):
        self._raise_if_invalid_cpf()

    def _raise_if_invalid_cpf(self) -> None:
        if self._is_invalid_cpf():
            raise InvalidCPFException()

    def _is_invalid_cpf(self) -> bool:
        if (
            not isinstance(self._cpf.value, str)
            or len(self._cpf.value) != 11
            or self._cpf.value == self._cpf.value[0] * 11
        ):
            return True

        def is_equal_to_verifying_digit(cpf_digit: int, remainder: int) -> bool:
            return cpf_digit == 0 if remainder < 2 else cpf_digit == 11 - remainder

        cpf_int_digits = [(int(digit)) for digit in self._cpf.value]
        first_remainder = (
            sum(
                cpf_digit * weight
                for cpf_digit, weight in zip(cpf_int_digits, range(10, 1, -1))
            )
            % 11
        )
        second_remainder = (
            sum(
                cpf_digit * weight
                for cpf_digit, weight in zip(cpf_int_digits, range(11, 1, -1))
            )
            % 11
        )
        return not (
            is_equal_to_verifying_digit(cpf_int_digits[9], first_remainder)
            and is_equal_to_verifying_digit(cpf_int_digits[10], second_remainder)
        )
