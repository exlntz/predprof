from fastapi import APIRouter,HTTPException,status,Depends,File,UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Annotated
import numpy as np
from app.core.database import SessionDep
from app.schemas.user import UserRegister,Token
import os
import uuid

ALLOWED_FILE_EXTENSIONS = {'npz'}
UPLOAD_DIR = "uploads"

router = APIRouter(prefix='/data', tags=['Загрузка файлов'])

@router.post("/upload-npz/")
async def upload_npz(file: UploadFile = File(...)):
    if not file.filename.endswith(".npz"):
        return {"error": "допустимы только .npz файлы"}

    file_path = os.path.join(UPLOAD_DIR, str(uuid.uuid4().hex)+'.npz')

    # сохраняем файл
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # проверка что файл читается numpy
    try:
        data = np.load(file_path)
        arrays = list(data.keys())
    except Exception:
        return {"error": "Invalid NPZ file"}

    return {
        "filename": file.filename,
        "arrays_in_file": arrays
    }
    