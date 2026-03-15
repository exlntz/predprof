from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Annotated

from app.core.database import SessionDep
from app.models import UserModel
from app.core.security import get_password_hash,is_password_correct,create_access_token
from app.schemas.user import UserRegister,Token

ALLOWED_FILE_EXTENSIONS = {'npz'}

@router.post('/avatar', summary='загрузка набора данных для проверки работы модели')
async def upload_avatar(
        session: SessionDep,
        current_user: UserDep,
        file: UploadFile = File(...)
):

    filename = file.filename or ""
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""

    if not ext and file.content_type:
        ctype = file.content_type.split('/')[-1].lower()
        if 'heic' in ctype or 'heif' in ctype:
            ext = 'heic'
        elif ctype == 'octet-stream' and filename.lower().endswith('.heic'):
            ext = 'heic'

    if ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Формат {ext} не поддерживается. Разрешены: {", ".join(ALLOWED_FILE_EXTENSIONS)}'
        )

    