from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from admin.AdminAuth import AdminAuth
from admin.MessageAdmin import PendingMessageAdmin
from config.Database import db, token
from models.Base import Base
from routers.Message import message_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db.dispose()

app = FastAPI(lifespan=lifespan)
authentication_backend = AdminAuth(secret_key=token)
app.include_router(message_router)
admin = Admin(app, db.engine, authentication_backend=authentication_backend)
admin.add_view(PendingMessageAdmin)