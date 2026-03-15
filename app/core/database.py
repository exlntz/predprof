from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import Depends
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_async_engine('sqlite+aiosqlite:///database.db')

async_session = async_sessionmaker(engine)

class Model(AsyncAttrs, DeclarativeBase):
    pass

class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True,nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)


class FileModel(Model):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(backref="files")

async def get_db():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]