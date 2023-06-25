from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from my_food.adapters.postgresql.database import engine


class CRUDMixin:
    @classmethod
    def retrieve(cls, uuid: UUID):
        with Session(engine) as session:
            instance = session.execute(select(cls).filter_by(uuid=UUID(uuid))).first()
            return instance

    def save(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()

    def update(self):
        pass

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
