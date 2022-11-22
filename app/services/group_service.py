from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import group_busy_dao
from db.enums import WeekdaysEnum, LessonsEnum


def create_group_busy(db, input_data):
    input_data = input_data.dict()
    input_data["is_busy"]=True
    group_busy_dao.create(db, input_data)
    current_group_busy = group_busy_dao.check_busy(db, input_data)
    return current_group_busy

def set_group_busy(db, input_data):
    group_busy_dao.set_busy(db, input_data)
    return check_group_busy(db, input_data)

def check_group_busy(db, input_data):
    if type(input_data) is not dict:
        input_data = input_data.dict()
    group_busy = group_busy_dao.check_busy(db, input_data)
    return group_busy
