from datetime import datetime
import secrets

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import student_dao
from db.enums import AcademicYearsEnum, AcademicGroupsEnum


def create(db, input_data):
    created = []
    for d in input_data:
        d.registration_token=secrets.token_urlsafe(10)
        student = student_dao.create(db, d)
        created.append(student)
    return created

def get_by_id(db, user_id):
    return student_dao.get_by_id(db, user_id)

def get_by_group(db, group_number, skip, limit):
    input_data = dict_of(academic_group=group_number)
    students=student_dao.get_all_by(db, input_data, skip, limit)
    return students

def get_by_year(db, year_number, skip, limit):
    input_data = dict_of(academic_year=year_number)
    students=student_dao.get_all_by(db, input_data, skip, limit)
    return students

def patch(db, user_id, input_data):
    patch_data = [(k, v) for k, v in input_data.dict().items()]
    student_dao.patch(db, patch_data, user_id)
    return student_dao.get_by_id(db, user_id)

def delete(db, user_id):
    patch_data = ('deleted_at', datetime.utcnow)
    return student_dao.patch(db, patch_data, user_id)


# def get_all(db, skip, limit):
#     return student_dao.get_all(db, skip, limit)

# def get_by_name(db, first_name, second_name, last_name):
#     input_data = dict_of(first_name, second_name, last_name)
#     print(input_data)
#     student=student_dao.get_by(db, input_data)
#     return student
#
# def students_id_by_module(module_id: int):
#     '''takes module id as an input, outputs the list of corresponding students ids'''
#     students_id_by_module = student_dao.get_id_by_module(module_id)
#
#     students_list = [];
#
#     for instance in students_id_by_module:
#         students_list.append(instance['student_id']);
#
#     return students_list;
