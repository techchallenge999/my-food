from abc import ABC
from my_food.application.domain.compartilhado.interfaces.validator import InterfaceValidator


class InterfaceUsuario(ABC):
    _cpf: str
    _email: str
    _nome: str
    _senha: str
    _validator: InterfaceValidator

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
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, value: str):
        self._nome = value

    @property
    def senha(self) -> str:
        return self._senha

    @senha.setter
    def senha(self, value: str):
        self._senha = value

    @property
    def validator(self) -> InterfaceValidator:
        return self._validator
