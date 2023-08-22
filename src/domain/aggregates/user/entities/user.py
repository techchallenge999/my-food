from uuid import UUID, uuid4

from src.domain.aggregates.user.interfaces.entities import UserInterface
from src.domain.aggregates.user.interfaces.value_objects import (
    CpfInterface,
    EmailInterface,
    PasswordInterface,
)
from src.domain.aggregates.user.validators.user_validator import UserValidator
from src.domain.shared.interfaces.validator import ValidatorInterface
from src.interface_adapters.gateways.repositories.user import UserRepositoryInterface


class User(UserInterface):
    def __init__(
        self,
        cpf: CpfInterface,
        email: EmailInterface,
        name: str,
        password: PasswordInterface,
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
        return self._cpf.value

    @cpf.setter
    def cpf(self, cpf: CpfInterface):
        self._cpf = cpf

    @property
    def email(self) -> str:
        return self._email.value

    @email.setter
    def email(self, email: EmailInterface):
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def password(self) -> str:
        return self._password.value

    @password.setter
    def password(self, password: PasswordInterface):
        self._password = password

    @property
    def uuid(self) -> str:
        return str(self._uuid)

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def validator(self) -> ValidatorInterface:
        return self._validator
