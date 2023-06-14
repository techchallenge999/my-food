from my_food.application.domain.usuarios.Interfaces.usuario import UsuarioAbstrato
from my_food.application.domain.usuarios.validator.usuario_validator import (
    UsuarioValidator,
)


class Usuario(UsuarioAbstrato):
    def __init__(self, cpf, email, nome, senha):
        self.cpf = "".join(filter(str.isdigit, cpf))
        self.email = email
        self.nome = nome
        self.senha = senha
        self._validator = UsuarioValidator(self)
        self.validator.validate()
