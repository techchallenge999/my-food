from typing import Optional

from sqlalchemy.orm import Session

from my_food.adapters.postgresql.database import engine
from my_food.adapters.postgresql.models.usuario.usuario import ModelUsuario
from my_food.application.domain.agregado_usuario.interfaces.entidade_usuario import InterfaceUsuario
from my_food.application.domain.agregado_usuario.interfaces.repositorio_usuario import InterfaceRepositorioUsuario


class RepositorioUsuario(InterfaceRepositorioUsuario):
    def create(self, entity: InterfaceUsuario) -> None:
        with Session(engine) as session:
            novo_usuario = ModelUsuario(
                cpf=entity.cpf,
                email=entity.email,
                nome=entity.nome,
                senha=entity.senha,
            )
            session.add(novo_usuario)
            session.commit()

    def find(self, id_: str) -> InterfaceUsuario:
        with Session(engine) as session:
            usuario = session.query(ModelUsuario).filter_by(cpf=id_).first()
            return usuario

    def update(self, entity: InterfaceUsuario) -> None:
        with Session(engine) as session:
            usuario = session.query(ModelUsuario).filter_by(cpf=entity.cpf).first()
            if usuario:
                usuario.cpf = entity.cpf
                usuario.email = entity.email
                usuario.nome = entity.nome
                usuario.senha = entity.senha
                session.commit()

    def find_by_email(self, email: str) -> Optional[InterfaceUsuario]:
        with Session() as session:
            usuario = session.query(ModelUsuario).filter_by(email=email).first()
            return usuario
