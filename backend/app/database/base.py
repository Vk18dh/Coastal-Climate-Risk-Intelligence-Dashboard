"""
SQLAlchemy async declarative base.

All ORM models defined in Phase 3 will inherit from this Base class.
Combining AsyncAttrs with DeclarativeBase gives models async lazy-loading
support out of the box (SQLAlchemy 2.x async pattern).
"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """
    Project-wide SQLAlchemy base class.

    Usage (Phase 3+):
        from app.database.base import Base

        class MyModel(Base):
            __tablename__ = "my_table"
            ...
    """
    pass
