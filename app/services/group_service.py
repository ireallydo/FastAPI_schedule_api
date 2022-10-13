from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import *
from db.dto import *
from db.dao import group_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


enum_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5};

def translate_enum_weekday(db: Session, weekday: WeekdaysEnum):
    '''is used to support mutilingual databases while using latin for input
    takes a value from the enum model as an input
    returns the matching weekday value from the 'weekdays' table in db
    e.g. "Monday" will return a proper weekday name from database in accordance with the enum attribute value'''
    if str(WeekdaysEnum(weekday).name) in enum_dict.keys():
        day_id=enum_dict[str(WeekdaysEnum(weekday).name)];
        db_weekday = db.query(WeekdayModel.name).where(WeekdayModel.id==day_id).all();
    return db_weekday[0][0];

# -----------------------------------------------------------------
# tech create functions
# -----------------------------------------------------------------

def set_group_busy(group_id: int, weekday: str, lesson: int):
    '''takes group id, weekday (str) and lesson number as input
    sets the is_busy flag to true'''
    return goup_dao.set_busy(group_id, weekday, lesson)

# -----------------------------------------------------------------
# tech read functions
# -----------------------------------------------------------------

# def get_group_id_by_number(group: int):
#     '''takes a group number as input, returns group id as an int'''
#     request_group_id = group_dao.get_id_by_number(group)
#     group_id = request_group_id[0][0];
#     return group_id;

def check_group_busy(group_number: int, weekday: WeekdaysEnum, lesson_number: int):
    '''takes group id, weekday (str) and lesson number as input
    returns false flag if the group is NOT busy and true flag is the group IS busy'''

    db_weekday = translate_enum_weekday(db, weekday);
    group_id = get_group_id_by_number(db, group_number);

    db_request = group_dao.check_busy(group_number, weekday, lesson_number)

    db_dict = db_request[0];

    if db_dict['is_busy']== False:
        return False;
    else:
        return True;
