from src.domain.aggregates.user.interfaces.value_objects import PasswordInterface
from src.domain.shared.exceptions.user import InvalidPasswordException
from src.domain.shared.interfaces.validator import ValidatorInterface


class PasswordValidator(ValidatorInterface):
    def __init__(self, entity: PasswordInterface):
        self._password = entity

    def validate(self):
        self._raise_if_invalid_password()

    def _raise_if_invalid_password(self) -> None:
        if self._is_invalid_password():
            raise InvalidPasswordException()

    def _is_invalid_password(self) -> bool:
        return not (
            isinstance(self._password.value, str) and len(self._password.value) >= 8
        )
