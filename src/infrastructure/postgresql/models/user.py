import uuid

from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.postgresql.database import Base
from src.infrastructure.postgresql.repositories.mixins import CRUDMixin


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base, CRUDMixin):
    __tablename__ = "user"

    cpf = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    name = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, index=True, default=False)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True)
    orders = relationship("OrderModel", lazy="subquery")
    id = Column(Integer, primary_key=True)

    def create(self) -> None:
        self.password = self.hash_password(self.password)
        super().create()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
