from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.RoomBusyModel import RoomBusyModel
from db.enums import WeekdaysEnum, LessonsEnum
from db.dto import *
from .base_dao import BaseDAO


class RoomBusyDAO(BaseDAO[RoomBusyModel, RoomBusyDTO, None, None]):

    def check_busy(self, db: Session, room_id, weekday, lesson):
        response = db.query(RoomBusyModel).filter(RoomBusyModel.room_id==room_id,
                                                               RoomBusyModel.weekday==weekday,
                                                               RoomBusyModel.lesson==lesson).first()
        return response

    def set_busy(self, db: Session, room_id, weekday, lesson):
        db.query(RoomBusyModel).filter(RoomBusyModel.room_id==room_id,
                                                   RoomBusyModel.weekday==weekday,
                                                   RoomBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch")
        db.commit()

room_busy_dao = RoomBusyDAO(RoomBusyModel)
