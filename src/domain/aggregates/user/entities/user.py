from uuid import UUID, uuid4

from src.domain.aggregates.user.interfaces.user_entity import (
    UserInterface,
)
from src.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from src.domain.aggregates.user.validators.user_validator import (
    UserValidator,
)
from src.domain.shared.interfaces.validator import ValidatorInterface


class User(UserInterface):
    def __init__(
        self,
        cpf: str,
        email: str,
        name: str,
        password: str,
        repository: UserRepositoryInterface,
        is_admin: bool = False,
        uuid: UUID = uuid4(),
    ):
        self.cpf = cpf
        self.email = email
        self.name = name
        self.password = password
        self._uuid = uuid
        self._is_admin = is_admin
        self._validator = UserValidator(self, repository)
        self.validator.validate()

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str):
        self._cpf = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator
