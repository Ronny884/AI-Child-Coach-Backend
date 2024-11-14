import uuid
from datetime import datetime

from sqlalchemy import String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BIGINT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func


class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class Child(Base):
    __tablename__ = 'children'

    child_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    thread: Mapped[str] = mapped_column(String(255))
    additional_instruction: Mapped[str] = mapped_column(Text)


