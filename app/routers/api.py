from fastapi import APIRouter
from . import authentication, schedule, users, modules, lessons, rooms, teachers, students, groups

api_router = APIRouter()

endpoints = [authentication, lessons, rooms, modules, groups, teachers, students, users, schedule]

for endpoint in endpoints:
    api_router.include_router(endpoint.router)
