from datetime import datetime

from sqlalchemy import Column, DateTime, func


class BaseTimestamp:
    __abstract__ = True
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __init__(self, *args, **kwargs):
        utcnow = datetime.utcnow()
        if "created_at" not in kwargs:
            kwargs["created_at"] = utcnow
        if "updated_at" not in kwargs:
            kwargs["updated_at"] = utcnow
        super().__init__(*args, **kwargs)
