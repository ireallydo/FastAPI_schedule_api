from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.ScheduleModel import ScheduleModel
from db.enums import LessonsEnum, WeekdaysEnum
from db.dto import *
from .base_dao import BaseDAO

class ScheduleDAO(BaseDAO[ScheduleModel, ScheduleCreateDTO, SchedulePatchDTO, ScheduleDeleteDTO]):


    def join_lessons_check(self, db: Session, teacher, module_id, input_data):
        return db.query(self.model).filter(self.model.teacher_id==teacher,
                                    self.model.semester==input_data.semester,
                                    self.model.weekday==input_data.wweekday,
                                    self.model.lesson_number==input_data.lesson_number,
                                    self.model.module_id==module_id,
                                    self.model.class_type==input_data.class_type).first()

    def fill_manually(self, db: Session, input_data: ScheduleCreateManuallyDTO):

        new_line = ScheduleCreateManuallyDTO(**input_data.dict())
        db.add(new_line)
        db.commit()

schedule_dao = ScheduleDAO(ScheduleModel)
