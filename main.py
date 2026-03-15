from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from contextlib import asynccontextmanager
from app.core.database import engine, Model




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
@app.get('/')
async def start():
    return 'privet'
