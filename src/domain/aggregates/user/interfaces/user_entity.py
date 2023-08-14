from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.shared.interfaces.validator import ValidatorInterface


class UserInterface(ABC):
    _cpf: str
    _email: str
    _name: str
    _password: str
    _is_admin: bool
    _uuid: UUID
    _validator: ValidatorInterface

    @property
    @abstractmethod
    def cpf(self) -> str:
        pass

    @cpf.setter
    @abstractmethod
    def cpf(self, value: str):
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @email.setter
    @abstractmethod
    def email(self, value: str):
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
    def password(self, value: str):
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
