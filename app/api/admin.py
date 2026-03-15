from fastapi import APIRouter
from app.schemas.user import UserRegister, Token
from app.core.database import SessionDep
from passlib.context import CryptContext
from app.core.database import User
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter,HTTPException,status,Depends,status, Body

router = APIRouter(prefix='/admin', tags=['Админка'])

pwd_context =CryptContext(schemes=['argon2'],deprecated='auto')

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post('/createuser', summary='Добавление пользователей')
async def create_user(
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