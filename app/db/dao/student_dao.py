from fastapi import HTTPException
from db.models.StudentModel import StudentModel
from db.dto import *
from .base_dao import BaseDAO


class StudentDAO(BaseDAO[StudentModel, StudentCreateDTO, StudentPatchDTO, None]):

    def check_user(self, input_data):
        try:
            student = db.query(self._model).filter_by(**input_data).first()
            assert (student is not None)
            return student
        except AssertionError:
            raise HTTPException(status_code=403, detail="Student was not found. Please contact your administrator.")


student_dao = StudentDAO(StudentModel)
