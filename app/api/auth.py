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
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
    )
    try:
        session.add(user_db)
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
    query=select(UserModel).where(UserModel.username == str(form_data.username))
    result=await session.execute(query)
    user=result.scalar_one_or_none()
    if not user or not is_password_correct(form_data.password,user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверная почта или пароль!'
        )
    token=create_access_token(data={'sub': user.username})

    return Token(access_token=token,token_type='bearer')
