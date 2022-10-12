from fastapi import APIRouter
from . import schedule, module, teacher, lesson, room, user

api_router = APIRouter()

endpoints = [schedule, module, teacher, lesson, room, user]

for endpoint in endpoints:
    api_router.include_router(endpoint.router)
