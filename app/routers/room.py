from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import group_service, room_service, schedule_service, teacher_service, user_service, module_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["room"])

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();
