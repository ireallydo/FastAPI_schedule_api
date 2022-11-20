from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import user_dao

import utils


def create(db, input_data):
    input_data.password = utils.hash_password(input_data.password)
    return user_dao.create(db, input_data)

def get_all(db, skip, limit):
    return user_dao.get_all(db, skip, limit)

def patch(db, search_data, patch_data):
    user = user_dao.get_by(db, search_data)
    user_dao.patch(db, patch_data, user.id)
    return user_dao.get_by_id(db, user.id)

def set_inactive(db, id):
    user_dao.set_inactive(db, id)
    return user_dao.get_by_id(db, id)

def get_by_login(db, login):
    user = user_dao.get_by_login(db, login)
    print(user)
    return user
# def get_user_by_id(user_id: int):
#     return user_dao.get_by_id(db=db, user_id=user_id)
#
# def get_user_by_email(email:str):
#     return user_dao.get_by_email(db=db, email=email)
#
# def get_users(skip: int = 0, limit: int = 100):
#     return user_dao.get_(db=db, skip=0, int=100)
