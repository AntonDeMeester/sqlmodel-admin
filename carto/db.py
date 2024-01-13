from sqlalchemy import create_engine
from sqlmodel import SQLModel

engine = create_engine("sqlite:///foo.db", echo=True)


def setup():
    create_all_models()


def create_all_models():
    from carto import models

    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
