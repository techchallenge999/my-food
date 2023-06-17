from sqlalchemy import Column, String
from my_food.adapters.postgresql.database import Base


class ModelUsuario(Base):
    __tablename__ = 'usuario'

    cpf = Column(String, index=True, primary_key=True)
    email = Column(String, index=True, unique=True)
    nome = Column(String)
    senha = Column(String)
