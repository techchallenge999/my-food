import re
from uuid import UUID

from src.domain.aggregates.user.interfaces.entities import (
    UserInterface,
)
from src.interface_adapters.gateways.repositories.user import (
    UserRepositoryInterface,
)
from src.domain.shared.exceptions.base import (
    InvalidUUIDException,
    UnavailableUUIDException,
)
from src.domain.shared.exceptions.user import (
    InvalidEmailException,
    InvalidPasswordException,
    UnavailableCPFException,
)
from src.domain.shared.interfaces.validator import ValidatorInterface


class UserValidator(ValidatorInterface):
    def __init__(self, entity: UserInterface, repository: UserRepositoryInterface):
        self._user = entity
        self._repository = repository

    def validate(self):
        self._raise_if_unavailable_cpf()
        self._raise_if_invalid_email()
        self._raise_if_unavailable_email()
        self._raise_if_invalid_password()
        self._raise_if_invalid_uuid()

    def _raise_if_unavailable_cpf(self) -> None:
        if self._is_unavailable_cpf():
            raise UnavailableCPFException()

    def _raise_if_invalid_email(self) -> None:
        if self._is_invalid_email():
            raise InvalidEmailException()

    def _raise_if_unavailable_email(self) -> None:
        if self._is_unavailable_email():
            raise UnavailableUUIDException()

    def _raise_if_invalid_password(self) -> None:
        if self._is_invalid_password():
            raise InvalidPasswordException()

    def _raise_if_invalid_uuid(self) -> None:
        if self._is_invalid_uuid():
            raise InvalidUUIDException()

    def _is_unavailable_cpf(self) -> bool:
        existent_user = self._repository.find_by_cpf(self._user.cpf)
        return existent_user is not None and existent_user.uuid != self._user.uuid

    def _is_invalid_email(self) -> bool:
        if not isinstance(self._user.email, str):
            return True
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(email_pattern, self._user.email) is None

    def _is_unavailable_email(self) -> bool:
        existent_user = self._repository.find_by_email(self._user.email)
        return existent_user is not None and existent_user.uuid != self._user.uuid

    def _is_invalid_password(self) -> bool:
        return not (
            isinstance(self._user.password, str) and len(self._user.password) >= 8
        )

    def _is_invalid_uuid(self) -> bool:
        try:
            return not isinstance(UUID(self._user.uuid), UUID)
        except ValueError:
            return True
