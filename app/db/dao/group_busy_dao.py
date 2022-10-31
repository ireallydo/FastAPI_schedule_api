from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.GroupBusyModel import GroupBusyModel
from db.enums import WeekdaysEnum, LessonsEnum
from db.dto import *
from .base_dao import BaseDAO

class GroupBusyDAO(BaseDAO[GroupBusyModel, GroupBusyDTO, None, None]):

    def check_busy(self, db: Session, input_data):
        response = db.query(GroupBusyModel).filter_by(**input_data).first()
        return response

    def set_busy(self, db: Session, input_data):
        db.query(GroupBusyModel).filter_by(**input_data).update({'is_busy': True}, synchronize_session="fetch")
        db.commit()

group_busy_dao = GroupBusyDAO(GroupBusyModel)


# def set_busy(db: Session, group_id: int, weekday: str, lesson: int):
#     db.query(GroupBusyModel).filter(GroupBusyModel.group_id==group_id,
#                                              GroupBusyModel.weekday==weekday,
#                                              GroupBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
#     db.commit();
#
# def check_busy(db:Session, group_number: int, weekday: WeekdaysEnum, lesson_number: int):
#     return db.query(GroupBusyModel.is_busy).where(GroupBusyModel.group_id==group_id,
#                                                            GroupBusyModel.weekday==db_weekday,
#                                                            GroupBusyModel.lesson==lesson_number).all();
#
#
# #group_dao = GroupDao()
