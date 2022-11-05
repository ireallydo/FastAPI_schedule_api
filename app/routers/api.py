from fastapi import APIRouter
from . import schedule, module, lesson, room, student, group, user, authentication

api_router = APIRouter()

endpoints = [schedule, module, lesson, room, student, group, user, authentication]

for endpoint in endpoints:
    api_router.include_router(endpoint.router)
