from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.TeacherBusyModel import TeacherBusyModel
from db.enums import WeekdaysEnum, LessonsEnum
from db.dto import *
from .base_dao import BaseDAO


class TeacherBusyDAO(BaseDAO[TeacherBusyModel, TeacherBusyDTO, None, None]):

    pass 

teacher_busy_dao = TeacherBusyDAO(TeacherBusyModel)
