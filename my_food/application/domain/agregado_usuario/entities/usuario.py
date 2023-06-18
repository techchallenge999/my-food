from my_food.application.domain.agregado_usuario.interfaces.entidade_usuario import (
    InterfaceUsuario,
)
from my_food.application.domain.agregado_usuario.interfaces.repositorio_usuario import (
    InterfaceRepositorioUsuario,
)
from my_food.application.domain.agregado_usuario.validators.usuario_validator import (
    UsuarioValidator,
)


class Usuario(InterfaceUsuario):
    def __init__(
        self,
        cpf: str,
        email: str,
        nome: str,
        senha: str,
        repository: InterfaceRepositorioUsuario,
    ):
        self.cpf = "".join(filter(str.isdigit, cpf))
        self.email = email
        self.nome = nome
        self.senha = senha
        self._validator = UsuarioValidator(self, repository)
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
    def validator(self) -> UsuarioValidator:
        return self._validator
