from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import lesson_dao
from db.enums import LessonsEnum

def create(db, input_data):
    return lesson_dao.create(db, input_data)

def get_all(db, skip, limit):
    return lesson_dao.get_all(db, skip, limit)

def patch(db, search_data, patch_data):
    lesson = lesson_dao.get_by(db, search_data)
    lesson_dao.patch(db, patch_data, lesson.id)
    return lesson_dao.get_by_id(db, lesson.id)

def delete(db, input_data):
    lesson = lesson_dao.get_by(db, input_data)
    return lesson_dao.delete(db, lesson.id)

def get_time_by_number(db, lesson_number):
    return lesson_dao.get_time_by_number(db, lesson_number)
