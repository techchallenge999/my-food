from abc import ABC, abstractmethod
from uuid import UUID
from my_food.application.domain.shared.interfaces.validator import InterfaceValidator


class UserInterface(ABC):
    _cpf: str
    _email: str
    _name: str
    _password: str
    _uuid: UUID
    _validator: InterfaceValidator

    @abstractmethod
    @property
    def cpf(self) -> str:
        pass

    @abstractmethod
    @cpf.setter
    def cpf(self, value: str):
        pass

    @abstractmethod
    @property
    def email(self) -> str:
        pass

    @abstractmethod
    @email.setter
    def email(self, value: str):
        pass

    @abstractmethod
    @property
    def name(self) -> str:
        pass

    @abstractmethod
    @name.setter
    def name(self, value: str):
        pass

    @abstractmethod
    @property
    def password(self) -> str:
        pass

    @abstractmethod
    @password.setter
    def password(self, value: str):
        pass

    @abstractmethod
    @property
    def uuid(self) -> UUID:
        pass

    @abstractmethod
    @uuid.setter
    def uuid(self, value: UUID):
        pass

    @abstractmethod
    @property
    def validator(self) -> InterfaceValidator:
        pass
