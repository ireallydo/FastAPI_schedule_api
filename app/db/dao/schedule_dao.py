from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.ScheduleModel import ScheduleModel
from db.enums import LessonsEnum, WeekdaysEnum
from db.dto import *
from .base_dao import BaseDAO

class ScheduleDAO(BaseDAO[ScheduleModel, ScheduleCreateDTO, SchedulePatchDTO, ScheduleDeleteDTO]):
    pass

schedule_dao = ScheduleDAO(ScheduleModel)
