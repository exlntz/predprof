from typing import Annotated
from fastapi import Depends,HTTPException,status
import jwt
from app.core.database import SessionDep
from app.core.database import User
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from dotenv import load_dotenv
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))



async def get_current_user(
        session: SessionDep,
        token: Annotated[str, Depends(oauth2_scheme)]
) -> User:

    unauthorized_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Некорректный токен или время сессии истекло',
        headers={"WWW-Authenticate": "Bearer"},  # Помогает браузеру понять тип авторизации
    )

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id: int | None = payload.get('sub')

        if user_id is None:
            raise unauthorized_error
    except:
        raise unauthorized_error

    query=select(User).where(User.id == int(user_id))
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise unauthorized_error

    return user


async def validate_admin_access(
        current_user: Annotated[User,Depends(get_current_user)]
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав.'
        )
    return current_user


UserDep = Annotated[User, Depends(get_current_user)]

AdminDep = Annotated[User, Depends(validate_admin_access)]