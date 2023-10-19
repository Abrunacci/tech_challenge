"""src/main.py
FastAPI initialization
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routers import all_routers

app = FastAPI()

for router in all_routers:
    app.include_router(router, prefix='/api', )


@app.get('/')
def root() -> RedirectResponse:
    return RedirectResponse(url='/docs')
