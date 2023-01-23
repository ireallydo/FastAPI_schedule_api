from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of
import secrets

from db.models import *
from db.dto import *
from db.dao import teacher_dao, teacher_busy_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


def create(db, input_data):
    created = []
    print(input_data)
    for d in input_data:
        d.registration_token=secrets.token_urlsafe(10)
        teacher = teacher_dao.create(db, d)
        created.append(teacher)
    return created

def get_all(db, skip, limit):
    return teacher_dao.get_all_by(db, skip, limit)

def get_profile(db, user_id):
    print(user_id)
    return teacher_dao.get_by_id(db, user_id)

def delete(db, user_id):
    patch_data = TeacherDeleteDTO(deleted_at=datetime.utcnow())
    return teacher_dao.patch(db, patch_data, user_id)


def get_teacher_by(db, teacher_data):
    teacher=teacher_dao.get_by(db, teacher_data)
    return teacher


def set_teacher_busy(db, user_id, input_data):
    check_data = input_data.dict().update(teacher_id=user_id)
    teacher_busy = teacher_busy_dao.get_by(db, check_data)
    if teacher_busy != None:
        try:
            assert (teacher_busy.is_busy == False)
            patch_data = [(k, v) for k, v in input_data.dict().items()]
            teacher_busy_dao.patch(db, patch_data, user_id)
        except AssertionError:
            raise HTTPException(status_code=404, detail="The teacher is already busy at this time.")
    else:
        input_data.dict().update(teacher_id=user_id)
        teacher_busy_dao.create(db, input_data)
    return teacher_busy_dao.get_by_id(db, user_id)


def create_modules(db, user_id, input_data):
    for module in input_data:
        create_dict = dict_of(teacher_id=id, module_id=module)
        teachers_dao.post(db, input_data)
    modules = get_modules(db, user_id)

def get_modules(db, user_id):
    response = teacher_dao.get_modules(db, user_id)
    return response

def delete_modules(db, user_id, input_data):
    modules = input_data.values()[0]
    for module in modules:
        teacher_dao.delete_module(db, user_id, module)


def get_teachers_by_module(db, module_id):
    '''takes module id as an input, outputs the list of corresponding teachers ids'''
    response = teachers_to_modules_dao.get_teachers_by_module(db, module_id)
    print('TEACHERS IDS FROM SERVICE')
    print(response)
    return response
