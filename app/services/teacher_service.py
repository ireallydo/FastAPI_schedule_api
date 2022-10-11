from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import *
from db.dto import *
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


enum_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5};

# -----------------------------------------------------------------
# tech create functions
# -----------------------------------------------------------------

def set_teacher_busy(db:Session, teacher_id: int, weekday: str, lesson: int):
    '''takes teacher id, weekday (str) and lesson number as input
    sets the is_busy flag to true'''

    db.query(TeacherBusyModel).filter(TeacherBusyModel.teacher_id==teacher_id,
                                             TeacherBusyModel.weekday==weekday,
                                             TeacherBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
    db.commit();

# -----------------------------------------------------------------
# tech read functions
# -----------------------------------------------------------------


def teachers_id_by_module(db: Session, module_id: int):
    '''takes module id as an input, outputs the list of corresponding teachers ids'''
    teachers_id_by_module = db.query(teachers_to_modules).where(teachers_to_modules.c.Module_id==module_id).all();

    teachers_list = [];

    for instance in teachers_id_by_module:
        teachers_list.append(instance['Teacher_id']);

    return teachers_list;


def check_teacher_busy(db: Session, teacher_id: int, weekday: str, lesson: int):
    '''takes teacher id, weekday (str) and lesson number as input
    returns false flag if the teacher is NOT busy and true flag is the teacher IS busy'''

    db_request = db.query(TeacherBusyModel.is_busy).where(TeacherBusyModel.teacher_id==teacher_id,
                                                           TeacherBusyModel.weekday==weekday,
                                                           TeacherBusyModel.lesson==lesson).all();

    db_dict = db_request[0];

    if db_dict['is_busy']== False:
        return False;
    else:
        return True;
