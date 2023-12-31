from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.aggregates.user.interfaces.value_objects import (
    CpfInterface,
    EmailInterface,
    PasswordInterface,
)
from src.domain.shared.interfaces.validator import ValidatorInterface


class UserInterface(ABC):
    _cpf: CpfInterface
    _email: EmailInterface
    _name: str
    _password: PasswordInterface
    _is_admin: bool
    _uuid: UUID
    _validator: ValidatorInterface

    @property
    @abstractmethod
    def cpf(self) -> str:
        pass

    @cpf.setter
    @abstractmethod
    def cpf(self, cpf: CpfInterface):
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @email.setter
    @abstractmethod
    def email(self, email: EmailInterface):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str):
        pass

    @property
    @abstractmethod
    def password(self) -> str:
        pass

    @password.setter
    @abstractmethod
    def password(self, password: PasswordInterface):
        pass

    @property
    @abstractmethod
    def is_admin(self) -> bool:
        pass

    @property
    @abstractmethod
    def uuid(self) -> str:
        pass

    @property
    @abstractmethod
    def validator(self) -> ValidatorInterface:
        pass
