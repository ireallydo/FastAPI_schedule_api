from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.UserModel import UserModel
from db.enums import AcademicYearsEnum, AcademicGroupsEnum
from db.dto import *
from .base_dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDTO, UserPatchDTO, None]):

    def get_by_login(self, db, login):
        response = db.query(UserModel).filter(UserModel.login==login).offset(skip).limit(limit).all()
        print(response)
        return response
    #
    # def get_by_year(self, db, year_number, skip, limit):
    #     response = db.query(StudentModel).filter(StudentModel.academic_year==year_number).offset(skip).limit(limit).all()
    #     print(response)
    #     return response

user_dao = UserDAO(UserModel)

#class UserDao:

# def get_by_id(db: Session, user_id: int):
#     return db.query(UserModel).filter(UserModel.id == user_id).first()
#
# def get_by_email(db:Session, email: str):
#     return db.query(UserModel).filter(UserModel.email == email).first()
#
# def get_users(db: Session, skip: int, limit: int):
#     return db.query(UserModel).offset(skip).limit(limit).all()

#user_dao = UserDao()
