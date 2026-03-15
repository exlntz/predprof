from app.schemas.user import UserRegister, Token
from fastapi import APIRouter,HTTPException,status,Depends,status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from app.core.database import SessionDep
from app.core.database import User
from typing import Annotated
from sqlalchemy import select
from datetime import timedelta,datetime,timezone
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

router = APIRouter(prefix='/auth', tags=['Авторизация'])


pwd_context =CryptContext(schemes=['argon2'],deprecated='auto')

def create_token(data: dict, expires_delta: timedelta, token_type: str):

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "iat": datetime.now(timezone.utc),
        "exp": expire,
        "type": token_type,
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(data: dict):
    return create_token(
        data=data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        token_type="access"
    )

def create_refresh_token(data: dict):
    return create_token(
        data=data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        token_type="refresh"
    )


def verify_refresh_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Ошибка token payload")

        return int(user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")

def get_password_hash(password):
    return pwd_context.hash(password)

def is_password_correct(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


@router.post('/register', summary='Регистрация')
async def register_user(
        user: UserRegister,
        session: SessionDep
):
    if user.password != user.password_repeat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Пароли не совпадают')

    hashed_password = get_password_hash(password=user.password)

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
    )
    try:
        session.add(new_user)
        await session.commit()

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователем с таким логином уже существует'
        )

    return {'message': 'Пользователь создан'}


@router.post('/login',summary='Логин')
async def login_user(
        session: SessionDep,
        form_data: Annotated[OAuth2PasswordRequestForm,Depends()]
) -> Token:
    query=select(User).where(User.username == str(form_data.username))
    result=await session.execute(query)
    user=result.scalar_one_or_none()
    if not user or not is_password_correct(form_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль!'
        )
    token=create_access_token(data={'sub': user.username})

    return Token(access_token=token,token_type='bearer')
