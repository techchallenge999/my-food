from uuid import UUID, uuid4

from src.domain.aggregates.user.interfaces.entities import UserInterface
from src.domain.aggregates.user.interfaces.value_objects import (
    CpfInterface,
    EmailInterface,
    PasswordInterface,
)
from src.domain.aggregates.user.validators.user_validator import UserValidator
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
    def cpf(self):
        return self._cpf.value

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @property
    def email(self):
        return self._email.value

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def password(self):
        return self._password.value

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def is_admin(self):
        return self._is_admin

    @property
    def uuid(self):
        return str(self._uuid)

    @property
    def validator(self):
        return self._validator
