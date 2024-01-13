from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .views import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="carto/static"), name="static")
app.include_router(router)
