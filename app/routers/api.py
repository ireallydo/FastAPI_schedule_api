from fastapi import APIRouter
from . import schedule

api_router = APIRouter()

endpoints = [schedule]

for endpoint in endpoints:
    api_router.include_router(endpoint.router)
