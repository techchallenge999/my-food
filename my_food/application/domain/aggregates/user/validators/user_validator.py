import re
from uuid import UUID

from my_food.application.domain.aggregates.user.interfaces.user_entity import UserInterface
from my_food.application.domain.aggregates.user.interfaces.user_repository import UserRepositoryInterface
from my_food.application.domain.shared.interfaces.validator import InterfaceValidator


class UserValidator(InterfaceValidator):
    def __init__(self, entity: UserInterface, repository: UserRepositoryInterface) -> None:
        self._user = entity
        self._repository = repository

    def validate(self):
        self._raise_if_invalid_cpf()
        self._raise_if_unavailable_cpf()
        self._raise_if_invalid_email()
        self._raise_if_unavailable_email()
        self._raise_if_invalid_password()
        self._raise_if_invalid_uuid()
        self._raise_if_unavailable_uuid()

    def _raise_if_invalid_cpf(self) -> None:
        if self._is_invalid_cpf():
            raise ValueError('CPF inválido')

    def _raise_if_unavailable_cpf(self) -> None:
        if self._is_unavailable_cpf():
            raise ValueError('CPF indisponível')

    def _raise_if_invalid_email(self) -> None:
        if self._is_invalid_email():
            raise ValueError('Email inválido')

    def _raise_if_unavailable_email(self) -> None:
        if self._is_unavailable_email():
            raise ValueError('Email indisponível')

    def _raise_if_invalid_password(self) -> None:
        if self._is_invalid_password():
            raise ValueError('Senha inválida')

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise ValueError('uuid inválido')

    def _raise_if_unavailable_uuid(self) -> None:
        if self._is_unavailable_uuid():
            raise ValueError('uuid indisponível')

    def _is_invalid_cpf(self) -> bool:
        if (
            not isinstance(self._user.cpf, str)
            or len(self._user.cpf) != 11
            or self._user.cpf == self._user.cpf[0] * 11
        ):
            return True

        def is_equal_to_verifying_digit(cpf_digit: int, remainder: int) -> bool:
            return cpf_digit == 0 if remainder < 2 else cpf_digit == 11 - remainder

        cpf_int_digits = [(int(digit)) for digit in self._user.cpf]
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

    def _is_unavailable_cpf(self) -> bool:
        return self._repository.find_by_cpf(self._user.cpf) is not None

    def _is_invalid_email(self) -> bool:
        if not isinstance(self._user.email, str):
            return True
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(email_pattern, self._user.email) is None

    def _is_unavailable_email(self) -> bool:
        return self._repository.find_by_email(self._user.email) is not None

    def _is_invalid_password(self) -> bool:
        return not (isinstance(self._user.password, str) and len(self._user.password) >= 8)

    def _is_invalid_uuid(self) -> bool:
        return isinstance(self._user.uuid, UUID)

    def _is_unavailable_uuid(self) -> bool:
        return self._repository.find(str(self._user.uuid)) is not None
