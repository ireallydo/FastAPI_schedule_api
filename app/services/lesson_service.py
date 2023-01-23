from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import lesson_dao
from db.enums import LessonsEnum

def create_lesson(db, input_data):
    return lesson_dao.create(db, input_data)

def get_all(db, skip, limit):
    return lesson_dao.get_all_by(db, skip, limit)

def get_by_number(db, lesson_number):
    return lesson_dao.get_by_number(db, lesson_number)

def patch(db, lesson_number, input_data):
    lesson = lesson_dao.get_by_number(db, lesson_number)
    lesson_dao.patch(db, input_data, lesson.id)
    return get_by_number(db, lesson_number)

def delete(db, lesson_number):
    lesson = lesson_dao.get_by_number(db, lesson_number)
    return lesson_dao.delete(db, lesson.id)
