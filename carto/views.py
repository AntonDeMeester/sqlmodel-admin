from fastapi import APIRouter, Request, status, Form
from fastapi.responses import HTMLResponse, Response
from sqlmodel import Session, select, delete
from fastapi.templating import Jinja2Templates
from typing import Annotated

from .db import engine
from .models import EquitySnapshot

router = APIRouter()

templates = Jinja2Templates(directory="carto/templates")


@router.get("/snapshots", name="snapshots_list_get", response_class=HTMLResponse)
def get_shares_list(request: Request) -> HTMLResponse:
    with Session(engine) as session:
        statement = select(EquitySnapshot)
        snapshots = session.exec(statement).all()
    return templates.TemplateResponse(request=request, name="equity/snapshots.list.jinja2", context={"snapshots": snapshots})


@router.get("/snapshots/new", name="snapshots_new_get", response_class=HTMLResponse)
def get_shares_new(request: Request) -> HTMLResponse:
    with Session(engine) as session:
        statement = select(EquitySnapshot).order_by(EquitySnapshot.version.desc()).limit(1)
        version_item = session.exec(statement).first()
        version = version_item.version if version_item else 1

    return templates.TemplateResponse(request=request, name="equity/snapshots.new.jinja2", context={"version": version})


@router.post("/snapshots/new", name="snapshots_new_post", response_class=HTMLResponse)
def post_shares_new(request: Request, name: Annotated[str, Form()], version: Annotated[int, Form()]) -> HTMLResponse:
    with Session(engine) as session:
        snapshot = EquitySnapshot(organization_id=1, name=name, version=version)
        session.add(snapshot)
        session.commit()

        return Response(
            f"/snapshots/{snapshot.id}",
            status_code=status.HTTP_201_CREATED,
            headers={"HX-Redirect": f"/snapshots/{snapshot.id}"},
        )


@router.get("/snapshots/{id}", name="snapshots_details_get", response_class=HTMLResponse)
def get_shared_detail(id: int, request: Request) -> HTMLResponse:
    with Session(engine) as session:
        statement = select(EquitySnapshot).where(EquitySnapshot.id == id)
        snapshot = session.exec(statement).first()

    if snapshot is None:
        return HTMLResponse("Snapshot not found", status_code=status.HTTP_404_NOT_FOUND)

    return templates.TemplateResponse(request=request, name="equity/snapshots.detail.jinja2", context={"snapshot": snapshot})


@router.delete("/snapshots/{id}", name="snapshots_details_delete", response_class=Response)
def delete_shared_detail(id: int) -> HTMLResponse:
    with Session(engine) as session:
        statement = delete(EquitySnapshot).where(EquitySnapshot.id == id)
        session.exec(statement)
        session.commit()

    return Response(status_code=status.HTTP_200_OK)
