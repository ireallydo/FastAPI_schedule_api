from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from fastapi import HTTPException

from db.models import *
from db.dto import *
from db.dao import user_dao, student_dao, teacher_dao

import utils



def create(db, input_data):

    password = utils.hash_password(input_data.password)

    input_check = dict_of(input_data.first_name, input_data.second_name, input_data.last_name, input_data.birth_date)

    if input_data.role == 'student':
        student = student_dao.check_user(db, input_check)

        if student.registered_user == False:
            try:
                print(input_data.registration_token)
                print(student.registration_token)
                assert (input_data.registration_token == student.registration_token)

                input_data = dict_of(student.id, input_data.login, password, input_data.email, input_data.role)

            except AssertionError:
                raise HTTPException(status_code=403, detail="Registration token for provided user is incorrect")
        else:
            raise HTTPException(status_code=403, detail="User for this student is already registered. Please contact your administrator.")

    elif input_data.role == 'teacher':
        student = teacher_dao.check_user(db, input_check)
        try:
            assert (input_data.registration_token == student.registration_token)

            input_data = dict_of(student.id, input_data.login, password, input_data.email, input_data.role)

        except AssertionError:
            raise HTTPException(status_code=403, detail="Registration token for provided user is incorrect")

    elif input_data.role == 'admin':
        input_data.password = password

    else:
        raise HTTPException(status_code=404, detail="Provided user role is not acceptable.")

    return user_dao.create(db, input_data)


def get_profile(db, user_id):
    return user_dao.get_by_id(db, user_id)

def patch(db, user_id, input_data):
    patch_data = [(k, v) for k, v in input_data.dict().items()]
    user_dao.patch(db, patch_data, user_id)
    return user_dao.get_by_id(db, user_id)

def change_password(db, user_id, input_data):
    input_data.password = utils.hash_password(input_data.password)
    patch(db, user_id, input_data)

def block_unblock(db, user_id, input_data):
    patch(db, user_id, input_data)

def delete(db, user_id):
    input_data = ('is_active', False)
    patch(db, user_id, input_data)

def get_by_login(db, login):
    user = user_dao.get_by_login(db, login)
    return user


# def get_all(db, skip, limit):
#     return user_dao.get_all(db, skip, limit)
#
#
# def get_user_by_id(user_id: int):
#     return user_dao.get_by_id(db=db, user_id=user_id)
#
# def get_user_by_email(email:str):
#     return user_dao.get_by_email(db=db, email=email)
#
# def get_users(skip: int = 0, limit: int = 100):
#     return user_dao.get_(db=db, skip=0, int=100)
