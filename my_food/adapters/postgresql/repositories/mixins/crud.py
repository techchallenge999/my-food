from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from my_food.adapters.postgresql.database import engine


class CRUDMixin:
    @classmethod
    def retrieve(cls, uuid: str):
        with Session(engine) as session:
            instance = session.execute(select(cls).filter_by(uuid=UUID(uuid))).first()
            return instance

    def save(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()

    @classmethod
    def update(cls, attributes: dict):
        for attr in attributes:
            if not hasattr(cls, attr):
                raise ValueError(f"Invalid attribute {attr}")
        with Session(engine) as session:
            session.execute(update(cls), [attributes])
            session.commit()

    def destroy(self):
        with Session(engine) as session:
            session.delete(self)
            session.commit()
            return self

    @classmethod
    def retrieve_by_column(cls, column: str, value):
        if hasattr(cls, column):
            with Session(engine) as session:
                instance = session.execute(
                    select(cls).filter((getattr(cls, column) == value))
                ).first()
                return instance
        return None
