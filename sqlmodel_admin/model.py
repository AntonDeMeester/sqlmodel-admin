from typing import Any, ClassVar, Type, Union

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, select
from sqlmodel.main import FieldInfo

from .base import base_api_route_name, templates


class SQLModelAdmin:
    model: ClassVar[Type[SQLModel]]
    page_size: int = 30

    def __init_subclass__(cls, model: type[SQLModel]):
        cls.model = model

    @classmethod
    @property
    def basename(cls) -> str:
        return cls.model.__tablename__

    @classmethod
    def get_router(cls, engine: Union[AsyncEngine, Engine], extra_context: dict[str, Any]) -> APIRouter:
        route_namebase = f"{base_api_route_name}_{cls.basename}"
        router = APIRouter(prefix=f"/{cls.basename}")
        router.add_api_route(
            "",
            cls.get_list(engine, extra_context=extra_context),
            response_class=HTMLResponse,
            name=f"{route_namebase}_list",
        )
        router.add_api_route(
            "/create",
            cls.get_create_display(engine, extra_context=extra_context),
            response_class=HTMLResponse,
            name=f"{route_namebase}_create_display",
        )
        router.add_api_route(
            "/create",
            cls.get_create_display(engine, extra_context=extra_context),
            response_class=HTMLResponse,
            name=f"{route_namebase}_create_new",
        )
        return router

    @classmethod
    def get_list(cls, engine: Union[AsyncEngine, Engine], extra_context: dict[str, Any]):
        async def get_list_route(request: Request, page: int = 0):
            offset = cls.page_size * page
            if isinstance(engine, AsyncEngine):
                async with engine.connect() as conn:
                    statement = select(cls.model).offset(offset).limit(cls.page_size)
                    result = await conn.execute(statement)
                    data = result.all()
            else:
                with engine.connect() as conn:
                    statement = select(cls.model).offset(offset).limit(cls.page_size)
                    result = conn.execute(statement)
                    data = result.all()

            return templates.TemplateResponse(
                "list.html",
                context={
                    "request": request,
                    "data": data,
                    "fields": cls.model.model_fields.keys(),
                    "name": cls.basename,
                    **extra_context,
                },
            )

        return get_list_route

    @classmethod
    def get_create_display(cls, engine: Union[AsyncEngine, Engine], extra_context: dict[str, Any]):
        async def get_list_route(request: Request, page: int = 0):
            return templates.TemplateResponse(
                "create.html",
                context={
                    "request": request,
                    "fields": {name: map_field_to_input(field) for name, field in cls.model.model_fields.items()},
                    "name": cls.basename,
                    **extra_context,
                },
            )

        return get_list_route

    @classmethod
    def get_create_new(cls, engine: Union[AsyncEngine, Engine], extra_context: dict[str, Any]):
        async def get_list_route(request: Request, page: int = 0):
            return templates.TemplateResponse(
                "create.html",
                context={
                    "request": request,
                    "fields": {name: map_field_to_input(field) for name, field in cls.model.model_fields.items()},
                    "name": cls.basename,
                    **extra_context,
                },
            )

        return get_list_route


def map_field_to_input(field: FieldInfo) -> dict:
    return {
        "required": is_required(field),
        "type": get_input_type(field),
    }


def get_input_type(field: FieldInfo) -> str:
    if issubclass(str, field.annotation):
        return "text"
    if issubclass(int, field.annotation):
        return "number"
    return "text"


def is_required(field: FieldInfo) -> bool:
    return False
