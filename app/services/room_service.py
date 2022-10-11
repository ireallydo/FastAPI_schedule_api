from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import *
from db.dto import *
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


enum_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5};

# -----------------------------------------------------------------
# tech read functions
# -----------------------------------------------------------------

def get_room_number_by_id(db:Session, room_id: int):
    '''takes a room id and returns correspondig room number'''
    request_room_number = db.query(RoomModel.number).where(RoomModel.id==room_id);
    room_number = request_room_number[0][0];
    return room_number;

def check_room_busy(db: Session, weekday: str, lesson: int):
    '''takes weekday and lesson as input
    returns one room with is_busy flag set to false (empty room)'''

    db_request = db.query(RoomBusyModel).where(RoomBusyModel.weekday==weekday,
                                                 RoomBusyModel.lesson==lesson,
                                                 RoomBusyModel.is_busy==False).first();

    return db_request.room_id;
