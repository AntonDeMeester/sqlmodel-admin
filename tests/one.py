from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, SQLModel

from sqlmodel_admin.admin import AdminRouter
from sqlmodel_admin.model import SQLModelAdmin


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


class VillainAdmin(SQLModelAdmin, model=Hero):
    pass


app = FastAPI()
admin = AdminRouter()
admin.register(HeroAdmin)
admin.register(VillainAdmin)
app.include_router(admin)


def test_basics():
    pass
