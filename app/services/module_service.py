from sqlalchemy.orm import Session

from db.models import *
from db.dto import *
from db.dao import module_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


def fill(db, input_data):
    return module_dao.fill_table(db, input_data)

def get_all(db, skip, limit):
    return module_dao.get_all(db, skip, limit)

def get_by_name(db, module_name, skip, limit):
    return module_dao.get_by_name(db, module_name, skip, limit)

def patch(db, input_data):
    return module_dao.patch(db, input_data)

def delete(db, input_data):
    return module_dao.delete(db, input_data)
