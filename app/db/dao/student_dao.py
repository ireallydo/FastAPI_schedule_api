from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.StudentModel import StudentModel
from db.enums import AcademicYearsEnum, AcademicGroupsEnum
from db.dto import *
from .base_dao import BaseDAO


class StudentDAO(BaseDAO[StudentModel, StudentCreateDTO, StudentPatchDTO, StudentDeleteDTO]):

    def get_by_group(self, db, group_number, skip, limit):
        response = db.query(StudentModel).filter(StudentModel.academic_group==group_number).offset(skip).limit(limit).all()
        print(response)
        return response

    def get_by_year(self, db, year_number, skip, limit):
        response = db.query(StudentModel).filter(StudentModel.academic_year==year_number).offset(skip).limit(limit).all()
        print(response)
        return response

student_dao = StudentDAO(StudentModel)

    # def get_by_field(self, db, attribute, skip, limit):
    #     for _ in attribute:
    #         key = _
    #         value = attribute[_]
    #     response = db.query(self.model).filter_by(**attribute).offset(skip).limit(limit).all()
    #     return response
