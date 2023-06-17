from my_food.application.domain.agregado_usuario.interfaces.entidade_usuario import InterfaceUsuario
from my_food.application.domain.agregado_usuario.interfaces.repositorio_usuario import InterfaceRepositorioUsuario
from my_food.application.domain.agregado_usuario.validators.usuario_validator import UsuarioValidator


class Usuario(InterfaceUsuario):
    def __init__(self, cpf: str, email: str, nome: str, senha: str, repository: InterfaceRepositorioUsuario):
        self.cpf = ''.join(filter(str.isdigit, cpf))
        self.email = email
        self.nome = nome
        self.senha = senha
        self._validator = UsuarioValidator(self, repository)
        self.validator.validate()
