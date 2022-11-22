from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.RoomModel import RoomModel
from db.enums import LessonsEnum, WeekdaysEnum
from db.dto import *
from .base_dao import BaseDAO


class RoomDAO(BaseDAO[RoomModel, RoomCreateDTO, RoomPatchDTO, RoomDeleteDTO]):

    def get_room_by_number(self, db: Session, room_number):
        response = db.query(self.model).filter(self.model.room_number==room_number).first()
        return response

    def get_rooms_by_class_type(self, db:Session, class_type):
        response = db.query(self.model).filter(self.model.class_type==class_type).all()
        return response
    # def get_by_id(db: Session, room_id):
    #     return db.query(RoomModel.number).where(RoomModel.id==room_id)

room_dao = RoomDAO(RoomModel)
