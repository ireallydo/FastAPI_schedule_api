from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import student_dao
from db.enums import AcademicYearsEnum, AcademicGroupsEnum


def create(db, input_data):
    return student_dao.create(db, input_data)

def get_all(db, skip, limit):
    return student_dao.get_all(db, skip, limit)

def patch(db, search_data, patch_data):
    student = student_dao.get_by(db, search_data)
    student_dao.patch(db, patch_data, student.id)
    return student_dao.get_by_id(db, student.id)

def delete(db, input_data):
    student = student_dao.get_by(db, input_data)
    return student_dao.delete(db, student.id)

def get_by_name(db, first_name, second_name, last_name):
    input_data = dict_of(first_name, second_name, last_name)
    print(input_data)
    student=student_dao.get_by(db, input_data)
    return student

def get_by_group(db, group_number, skip, limit):
    students=student_dao.get_by_group(db, group_number, skip, limit)
    return students

def get_by_year(db, year_number, skip, limit):
    students=student_dao.get_by_year(db, year_number, skip, limit)
    print(students)
    return students

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
