import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from my_food.adapters.postgresql.database import Base
from my_food.adapters.postgresql.repositories.mixins.crud import CRUDMixin


class UserModel(Base, CRUDMixin):
    __tablename__ = "user"

    cpf = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    name = Column(String)
    password = Column(String)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    id = Column(Integer, primary_key=True)
