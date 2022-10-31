from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.LessonModel import LessonModel
from db.enums import LessonsEnum
from db.dto import *
from .base_dao import BaseDAO


class LessonDAO(BaseDAO[LessonModel, LessonCreateDTO, LessonPatchDTO, LessonDeleteDTO]):

    def get_time_by_number(self, db: Session, lesson_number):
        response = db.query(self.model).filter(self.model.lesson_number==lesson_number).first()
        return response

lesson_dao = LessonDAO(LessonModel)
