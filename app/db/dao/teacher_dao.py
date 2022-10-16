from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models import TeacherModel, TeacherBusyModel
from db.enums import WeekdaysEnum
from db.dto import *
from . import BaseDAO

class TeacherDAO(BaseDAO[TeacherModel, TeacherCreateDTO, TeacherPatchDTO, TeacherDeleteDTO]):

    def get_id_by_module(db: Session, module_id):
        return db.query(teachers_to_modules).where(teachers_to_modules.c.Module_id==module_id).all()

teacher_dao = TeacherDAO(TeacherModel)
