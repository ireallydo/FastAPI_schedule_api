from fastapi import APIRouter
from . import authentication, schedule, user, module, lesson, room, teacher, teacher_to_module, student, group

api_router = APIRouter()

endpoints = [authentication, schedule, user, module, lesson, room, teacher, teacher_to_module, student, group]

for endpoint in endpoints:
    api_router.include_router(endpoint.router)
