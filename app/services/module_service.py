from sorcery import dict_of

from sqlalchemy.orm import Session

from db.models import *
from db.dto import *
from db.dao import module_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


def create_module(db, input_data):
    return module_dao.create(db, input_data)

def get_all_modules(db, skip, limit):
    return module_dao.get_all_by(db, skip, limit)

def get_by_id(db, module_id):
    return module_dao.get_by_id(db, module_id)

def get_teachers(db, module_id):
    return module_dao.get_teachers(db, module_id)

def delete(db, module_id):
    module_dao.delete(db, module_id)

# def get_by_name(db, module_name, skip, limit):
#     return module_dao.get_all_by_name(db, module_name, skip, limit)
# def get_by_name_and_type(db, module_name, class_type):
#     input_data = dict_of(module_name, class_type)
#     return module_dao.get_by(db, input_data)
#
# def patch(db, search_data, patch_data):
#     module = module_dao.get_by(db, search_data)
#     module_dao.patch(db, patch_data, module.id)
#     return module_dao.get_by_id(db, module.id)
