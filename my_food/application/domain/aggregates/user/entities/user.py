from uuid import UUID, uuid4

from my_food.application.domain.aggregates.user.interfaces.user_entity import (
    UserInterface,
)
from my_food.application.domain.aggregates.user.interfaces.user_repository import (
    UserRepositoryInterface,
)
from my_food.application.domain.aggregates.user.validators.user_validator import (
    UserValidator,
)


class User(UserInterface):
    def __init__(
        self,
        cpf: str,
        email: str,
        name: str,
        password: str,
        repository: UserRepositoryInterface,
        uuid: UUID = uuid4(),
    ):
        self.cpf = "".join(filter(str.isdigit, cpf))
        self.email = email
        self.name = name
        self.password = password
        self._uuid = uuid
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
    def validator(self) -> UserValidator:
        return self._validator
