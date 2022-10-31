from fastapi import APIRouter
from . import schedule, module, lesson, room, student, group

api_router = APIRouter()

endpoints = [schedule, module, lesson, room, student, group]

for endpoint in endpoints:
    api_router.include_router(endpoint.router)
