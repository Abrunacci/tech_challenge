"""src.routers.movies
All the movies related routers
"""
from os import environ
import requests
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from src.schemas.movies import MovieSchema


router = APIRouter()


@router.post("/movies/seed", tags=['Movies'], status_code=201)
async def seed_movies() -> str:
    response = requests.get(environ.get('EXTERNAL_API_URL'))
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.reason)
    return "success"
