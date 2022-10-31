from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.TeacherModel import TeacherModel
from db.dto import *
from .base_dao import BaseDAO


class TeacherDAO(BaseDAO[TeacherModel, TeacherCreateDTO, TeacherPatchDTO, TeacherDeleteDTO]):

    def get_by_login(self, db, login):
        return db.query(TeacherModel).where(TeacherModel.login==login).all()

teacher_dao = TeacherDAO(TeacherModel)
