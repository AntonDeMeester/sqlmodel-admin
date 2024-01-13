from typing import Optional
import os

from fastapi import FastAPI

# from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine, AsyncSession
from sqlmodel import Field, SQLModel
from sqlalchemy import create_engine

from sqlmodel_admin.admin import AdminRouter
from sqlmodel_admin.model import SQLModelAdmin
import uvicorn


class Hero(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    civilian_name: Optional[str]
    backstory: Optional[str]


class HeroAdmin(SQLModelAdmin, model=Hero):
    pass


class Villain(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    civilian_name: Optional[str]
    backstory: Optional[str]


class VillainAdmin(SQLModelAdmin, model=Villain):
    pass


engine = create_engine("sqlite:///foo.db")

app = FastAPI()
admin = AdminRouter(engine)
admin.register(HeroAdmin)
admin.register(VillainAdmin)
app.mount("/admin", admin.subapp, name="admin")

hostname = f"{os.environ['CODESPACE_NAME']}.{os.environ['GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN']}"


def create_all_models():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)


def main():
    create_all_models()
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
