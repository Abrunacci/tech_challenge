"""src/main.py
FastAPI initialization
"""
from os import environ

from elasticsearch import Elasticsearch
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.routers import all_routers

app = FastAPI()
es = Elasticsearch(
    f"http://{environ.get('ELASTICSEARCH_HOST')}:{environ.get('ELASTICSEARCH_PORT')}"
)


for router in all_routers:
    app.include_router(
        router,
        prefix="/api",
    )


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
