from sorcery import dict_of

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import teacher_dao, teacher_busy_dao, teachers_to_modules_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum

from services import teacher_service, module_service

def get_teacher(db, input_data):
    if input_data.second_name:
        second_name=input_data.second_name;
    else:
        second_name=None
    teacher_data = dict_of(input_data.first_name, second_name, input_data.last_name)
    teacher = teacher_service.get_teacher_by(db, teacher_data)
    return teacher

def get_module(db, input_data):
    module = module_service.get_by_name_and_type(db, input_data.module_name, input_data.class_type)
    return module

def post_teacher_to_module(db, input_data):
    teacher = get_teacher(db, input_data)
    module = get_module(db, input_data)
    return teachers_to_modules_dao.post_teacher_to_module(db, teacher.id, module.id)

def get_all(db):
    result = teachers_to_modules_dao.get_all(db)
    output = []
    for _ in result:
        teacher = teacher_service.get_by_id(db, _.teacher_id)
        module = module_service.get_by_id(db, _.module_id)
        output.append(dict_of(teacher.first_name, teacher.second_name, teacher.last_name, module.module_name))
    return output

def delete_association(db, input_data):
    teacher = get_teacher(db, input_data)
    module = get_module(db, input_data)
    return teachers_to_modules_dao.delete(db, module.id, teacher.id)
