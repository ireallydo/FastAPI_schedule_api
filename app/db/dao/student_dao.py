from db.models.StudentModel import StudentModel
from db.dto import StudentCreateDTO, StudentPatchDTO
from .base_dao import BaseDAO


class StudentDAO(BaseDAO[StudentModel, StudentCreateDTO, StudentPatchDTO, None]):
    pass


student_dao = StudentDAO(StudentModel)
