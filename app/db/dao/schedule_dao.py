from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.ScheduleModel import ScheduleModel
from db.enums import LessonsEnum, WeekdaysEnum
from db.dto import *
from .base_dao import BaseDAO

class ScheduleDAO(BaseDAO[ScheduleModel, ScheduleCreateDTO, SchedulePatchDTO, ScheduleDeleteDTO]):

    def fill_manually(input_data: ScheduleCreateManuallyDTO):

        new_line = ScheduleCreateManuallyDTO(**input_data.dict())

        db.add(new_line)
        db.commit()
        db.refresh(new_line)

        return new_line

    def check_exists(db, input_data: ScheduleCreateManuallyDTO):

            return db.query(ScheduleModel).filter(ScheduleModel.group==input_data.group,
                                                ScheduleModel.semester==input_data.semester,
                                                ScheduleModel.weekday==input_data.weekday,
                                                ScheduleModel.lesson_number==input_data.lesson_number).all()

    def join_lessons_check(self, db, teacher, module_id, input_data):
        return db.query(self.model).filter(self.model.teacher_id==teacher,
                                    self.model.semester==input_data.semester,
                                    self.model.weekday==input_data.wweekday,
                                    self.model.lesson_number==input_data.lesson_number,
                                    self.model.module_id==module_id,
                                    self.model.class_type==input_data.class_type).first()

schedule_dao = ScheduleDAO(ScheduleModel)
