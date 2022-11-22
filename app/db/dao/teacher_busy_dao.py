from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.TeacherBusyModel import TeacherBusyModel
from db.enums import WeekdaysEnum, LessonsEnum
from db.dto import *
from .base_dao import BaseDAO


class TeacherBusyDAO(BaseDAO[TeacherBusyModel, TeacherBusyDTO, None, None]):

    def check_busy(self, db: Session, teacher_id, weekday, lesson):
        response = db.query(self.model).filter(self.model.teacher_id==teacher_id,
                                            self.model.weekday==weekday,
                                            self.model.lesson==lesson).first()
        return response

    def set_busy(self, db: Session, teacher_id, weekday, lesson):
        db.query(self.model).filter(self.model.teacher_id==teacher_id,
                                    self.model.weekday==weekday,
                                    self.model.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch")
        db.commit()

teacher_busy_dao = TeacherBusyDAO(TeacherBusyModel)
