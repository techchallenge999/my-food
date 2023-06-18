from sqlalchemy import Column, String
from my_food.adapters.postgresql.database import Base


class UserModel(Base):
    __tablename__ = 'user'

    cpf = Column(String, index=True, primary_key=True)
    email = Column(String, index=True, unique=True)
    name = Column(String)
    password = Column(String)
