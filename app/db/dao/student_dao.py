from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.StudentModel import StudentModel
from db.enums import AcademicYearsEnum, AcademicGroupsEnum
from db.dto import *
from .base_dao import BaseDAO


class StudentDAO(BaseDAO[StudentModel, StudentCreateDTO, StudentPatchDTO, None]):

    # def get_by_group(self, db, group_number, skip, limit):
    #     response = db.query(self.model).filter(StudentModel.academic_group==group_number).offset(skip).limit(limit).all()
    #     print(response)
    #     return response

    # def get_by_year(self, db, year_number, skip, limit):
    #     response = db.query(self.model).filter(StudentModel.academic_year==year_number).offset(skip).limit(limit).all()
    #     print(response)
    #     return response

    def check_user(self, db, input_data):
        try:
            student = db.query(self.model).filter_by(**input_data).first()
            # print(student)
            assert (student != None)
            return student
        except AssertionError:
            raise HTTPException(status_code=403, detail="Student was not found. Please contact your administrator.")

student_dao = StudentDAO(StudentModel)
