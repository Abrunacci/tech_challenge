"""src/main.py
FastAPI initialization
"""
import logging.config

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.routers import all_routers

app = FastAPI()

logging.config.fileConfig("/app/src/logging.conf", disable_existing_loggers=False)

log = logging.getLogger(__name__)

for router in all_routers:
    app.include_router(
        router,
        prefix="/api",
    )


@app.get("/")
def root() -> RedirectResponse:
    log.info("Redirecting to docs")
    return RedirectResponse(url="/docs")
