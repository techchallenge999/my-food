import re

from src.domain.aggregates.user.interfaces.value_objects import EmailInterface
from src.domain.shared.exceptions.user import InvalidCPFException
from src.domain.shared.interfaces.validator import ValidatorInterface


class EmailValidator(ValidatorInterface):
    def __init__(self, entity: EmailInterface):
        self._email = entity

    def validate(self):
        self._raise_if_invalid_email()

    def _raise_if_invalid_email(self) -> None:
        if self._is_invalid_email():
            raise InvalidCPFException()

    def _is_invalid_email(self) -> bool:
        if not isinstance(self._email.value, str):
            return True
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(email_pattern, self._email.value) is None
