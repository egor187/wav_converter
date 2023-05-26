from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    Uuid,
    MetaData,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, relationship
from uuid import uuid4

from settings import settings

engine = create_engine(settings.DB_URL)
metadata_obj = MetaData()
metadata_obj.create_all(engine)


class Base(DeclarativeBase):
    pass


class IDModel(Base):
    __abstract__ = True

    id = mapped_column(Integer, primary_key=True)


class TimeStampedModel(IDModel):
    __abstract__ = True

    created = mapped_column(DateTime, default=func.now())
    updated = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(TimeStampedModel):
    __tablename__ = "user"

    name = mapped_column(String, nullable=False, unique=True)
    token = mapped_column(Uuid, nullable=False, default=uuid4)
    files: Mapped[list["File"]] = relationship(back_populates="user")


class File(TimeStampedModel):
    __tablename__ = "file"

    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="files")
    path = mapped_column(String, nullable=False)


async def get_db():
    return Session(engine)


Base.metadata.create_all(engine)
