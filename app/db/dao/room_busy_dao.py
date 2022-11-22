from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.RoomBusyModel import RoomBusyModel
from db.enums import WeekdaysEnum, LessonsEnum
from db.dto import *
from .base_dao import BaseDAO


class RoomBusyDAO(BaseDAO[RoomBusyModel, RoomBusyDTO, None, None]):

    def check_busy(self, db: Session, room_id, weekday, lesson):
        response = db.query(self.model).filter(self.model.room_id==room_id,
                                            self.model.weekday==weekday,
                                            self.model.lesson==lesson).first()
        return response

    def set_busy(self, db: Session, room_id, weekday, lesson):
        db.query(self.model).filter(self.model.room_id==room_id,
                                    self.model.weekday==weekday,
                                    self.model.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch")
        db.commit()

    def get_spare_room(self, db:Session, weekday, lesson):
        return db.query(self.model).filter(self.model.weekday==weekday,
                                    self.model.lesson==lesson,
                                    self.model.is_busy==False).first()


room_busy_dao = RoomBusyDAO(RoomBusyModel)
