from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.TeacherBusyModel import TeacherBusyModel
from db.enums import WeekdaysEnum, LessonsEnum
from db.dto import *
from .base_dao import BaseDAO


class TeacherBusyDAO(BaseDAO[TeacherBusyModel, TeacherBusyDTO, None, None]):

    def check_busy(self, db: Session, teacher_id, weekday, lesson):
        response = db.query(TeacherBusyModel).filter(TeacherBusyModel.teacher_id==teacher_id,
                                                               TeacherBusyModel.weekday==weekday,
                                                               TeacherBusyModel.lesson==lesson).first()
        return response

    def set_busy(self, db: Session, teacher_id, weekday, lesson):
        db.query(TeacherBusyModel).filter(TeacherBusyModel.teacher_id==teacher_id,
                                                   TeacherBusyModel.weekday==weekday,
                                                   TeacherBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch")
        db.commit()

teacher_busy_dao = TeacherBusyDAO(TeacherBusyModel)
