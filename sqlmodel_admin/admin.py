from typing import Any, Type, TypedDict, Union

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from .base import base_api_route_name, templates
from .model import SQLModelAdmin


class GenericContext(TypedDict):
    model_names: list[str]


class AdminRouter:
    _admins: list[Type[SQLModelAdmin]]
    subapp: FastAPI
    local_context: dict[str, Any]

    def __init__(self, engine: Union[Engine, AsyncEngine]):
        super().__init__()
        self._admins = []
        self.subapp = FastAPI()
        self.engine = engine
        self.extra_context: GenericContext = {"model_names": []}

        self._add_generic_routes()

    def register(self, admin: Type[SQLModelAdmin]) -> None:
        self._admins.append(admin)
        self.extra_context["model_names"].append(admin.basename)
        self.subapp.include_router(admin.get_router(self.engine, extra_context=self.extra_context))

    def _add_generic_routes(self) -> None:
        self.subapp.mount("/static", StaticFiles(directory="sqlmodel_admin/static"), name="static")

        @self.subapp.get("", response_class=HTMLResponse, name=f"{base_api_route_name}_models_list")
        async def get_list_route(request: Request) -> HTMLResponse:
            return templates.TemplateResponse("models.html", context={"request": request, **self.extra_context})
