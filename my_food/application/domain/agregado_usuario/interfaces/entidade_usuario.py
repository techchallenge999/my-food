from abc import ABC, abstractmethod
from my_food.application.domain.compartilhado.interfaces.validator import (
    InterfaceValidator,
)


class InterfaceUsuario(ABC):
    _cpf: str
    _email: str
    _nome: str
    _senha: str
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
    def nome(self) -> str:
        pass

    @abstractmethod
    @nome.setter
    def nome(self, value: str):
        pass

    @abstractmethod
    @property
    def senha(self) -> str:
        pass

    @abstractmethod
    @senha.setter
    def senha(self, value: str):
        pass

    @abstractmethod
    @property
    def validator(self) -> InterfaceValidator:
        pass
