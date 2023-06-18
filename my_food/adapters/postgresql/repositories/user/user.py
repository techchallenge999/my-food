from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from my_food.adapters.postgresql.database import engine
from my_food.adapters.postgresql.models.user.user import UserModel
from my_food.application.domain.aggregates.user.interfaces.user_entity import UserInterface
from my_food.application.domain.aggregates.user.interfaces.user_repository import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):

    def create(self, entity: UserInterface) -> None:
        with Session(engine) as session:
            new_user = UserModel(
                cpf=entity.cpf,
                email=entity.email,
                name=entity.name,
                password=entity.password,
            )
            session.add(new_user)
            session.commit()

    def find(self, uuid: str) -> Optional[UserInterface]:
        with Session(engine) as session:
            user = session.query(UserModel).filter_by(uuid=UUID(uuid)).first()
            return user

    def update(self, entity: UserInterface) -> None:
        with Session(engine) as session:
            user = session.query(UserModel).filter_by(uuid=entity.uuid).first()
            if user:
                user.cpf = entity.cpf
                user.email = entity.email
                user.name = entity.name
                user.password = entity.password
                session.commit()

    def find_by_cpf(self, cpf: str) -> Optional[UserInterface]:
        with Session() as session:
            user = session.query(UserModel).filter_by(cpf=cpf).first()
            return user

    def find_by_email(self, email: str) -> Optional[UserInterface]:
        with Session() as session:
            user = session.query(UserModel).filter_by(email=email).first()
            return user
