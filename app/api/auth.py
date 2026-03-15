from app.schemas.user import UserRegister
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from app.core.database import SessionDep
from app.core.database import User

router = APIRouter(prefix='/auth', tags=['Авторизация'])


pwd_context =CryptContext(schemes=['argon2'],deprecated='auto')

def get_password_hash(password):
    return pwd_context.hash(password)

def is_pwd_correct(password, hashed_password):
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
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,

    )

    session.add(new_user)
    await session.commit()

    return {'message': 'Пользователь создан'}