from my_food.application.domain.usuarios.validator.usuario_validator import (
    UsuarioValidator,
)


class Usuario:
    def __init__(self, cpf, email, nome, senha):
        self.cpf: str = "".join(filter(str.isdigit, cpf))
        self.email: str = email
        self.nome: str = nome
        self.senha: str = senha
        self.validator = UsuarioValidator()
        self.validator.validate(self)
