from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends

engine = create_async_engine('sqlite+aiosqlite:///database.db')

async_session = async_sessionmaker(engine)

class Model(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]