from sqlmodel import SQLModel, Field, Relationship
import datetime
from sqlalchemy.sql import func
from typing import Optional


class TrackedModel(SQLModel):
    id: int = Field(primary_key=True)
    created_at: datetime.datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime.datetime = Field(sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()})


class Organization(TrackedModel, table=True):
    name: str

    # Back populates
    equity_snapshots: list["EquitySnapshot"] = Relationship(back_populates="organization")


class EquitySnapshot(TrackedModel, table=True):
    organization_id: int = Field(foreign_key="organization.id")
    organization: Organization = Relationship(back_populates="equity_snapshots")

    name: str
    version: int
    active: bool = False

    # Back populates
    equities: list["EquityAmount"] = Relationship(back_populates="snapshot")


class EquityAmount(TrackedModel, table=True):
    snapshot_id: int = Field(foreign_key="equitysnapshot.id")
    snapshot: EquitySnapshot = Relationship(back_populates="equities")

    shares: Optional[int] = None
    percentage: Optional[float] = None
