from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.orm import Session, subqueryload
from src.infrastructure.postgresql.database import engine
from src.domain.shared.errors.exceptions.order import (
    OrderNotFoundException,
)


class CRUDMixin:
    def create(self) -> None:
        with Session(engine) as session:
            session.add(self)
            session.commit()

    def self_destroy(self) -> None:
        with Session(engine) as session:
            session.delete(self)
            session.commit()

    @classmethod
    def retrieve(cls, uuid: str | None):
        if uuid is None:
            return None
        with Session(engine) as session:
            instance = session.execute(select(cls).filter_by(uuid=UUID(uuid))).first()
            return instance[0] if instance is not None else None

    @classmethod
    def update(cls, attributes: dict):
        for attr in attributes:
            if not hasattr(cls, attr):
                raise ValueError(f"Invalid attribute {attr}")
        with Session(engine) as session:
            session.execute(update(cls), [attributes])
            session.commit()

    @classmethod
    def destroy(cls, uuid: str):
        with Session(engine) as session:
            instance = session.execute(select(cls).filter_by(uuid=UUID(uuid))).first()
            if instance is None:
                raise OrderNotFoundException()
            session.delete(instance[0])
            session.commit()

    @classmethod
    def retrieve_by_column(cls, column: str, value):
        if not hasattr(cls, column):
            return None
        with Session(engine) as session:
            instance = session.execute(
                select(cls).filter((getattr(cls, column) == value))
            ).first()
            return instance[0] if instance is not None else None

    @classmethod
    def list(cls):
        with Session(engine) as session:
            instance = session.execute(select(cls)).all()
            return instance

    @classmethod
    def list_filtering_by_column(cls, filters: dict = {}, children: list = []):
        stmt = select(cls)
        for child in children:
            if hasattr(cls, child):
                stmt = stmt.options(subqueryload(getattr(cls, child)))
        for column in filters.keys():
            if not hasattr(cls, column):
                return None
            stmt = stmt.filter((getattr(cls, column) == filters.get(column)))
        with Session(engine) as session:
            instance = session.execute(stmt).all()
            return instance
