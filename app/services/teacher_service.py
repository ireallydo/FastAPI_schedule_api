from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import teacher_dao, teacher_busy_dao, teachers_to_modules_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


def create(db, input_data):
    return teacher_dao.create(db, input_data)

def get_all(db, skip, limit):
    return teacher_dao.get_all(db, skip, limit)

def patch(db, search_data, patch_data):
    teacher = teacher_dao.get_by(db, search_data)
    teacher_dao.patch(db, patch_data, teacher.id)
    return teacher_dao.get_by_id(db, teacher.id)

def delete(db, input_data):
    teacher = teacher_dao.get_by(db, input_data)
    return teacher_dao.delete(db, teacher.id)

def get_teacher_by(db, teacher_data):
    teacher=teacher_dao.get_by(db, teacher_data)
    return teacher

def get_by_id(db, teacher_id):
    teacher=teacher_dao.get_by_id(db, teacher_id)
    return teacher

def check_teacher_busy(db, teacher_id, weekday, lesson):
    teacher_busy = teacher_busy_dao.check_busy(db, teacher_id, weekday, lesson)
    return teacher_busy

def create_teacher_busy(db, teacher_id, weekday, lesson):
    input_data = dict_of(teacher_id, weekday, lesson)
    input_data["is_busy"]=True
    teacher_busy_dao.create(db, input_data)
    return check_teacher_busy(db, teacher_id, weekday, lesson)

def set_teacher_busy(db, teacher_id, weekday, lesson):
    teacher_busy_dao.set_busy(db, teacher_id, weekday, lesson)
    return check_teacher_busy(db, teacher_id, weekday, lesson)

def get_teachers_by_module(db, module_name):
    '''takes module id as an input, outputs the list of corresponding teachers ids'''

    teachers_to_modules_dao.get_teachers_by_module(db, module_id)


#
# def teachers_id_by_module(module_id: int):
#     '''takes module id as an input, outputs the list of corresponding teachers ids'''
#     teachers_id_by_module = teacher_dao.get_id_by_module(module_id)
#
#     teachers_list = [];
#
#     for instance in teachers_id_by_module:
#         teachers_list.append(instance['Teacher_id']);
#
#     return teachers_list;
