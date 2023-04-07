import secrets
from fastapi import HTTPException
from http import HTTPStatus
from typing import List, NoReturn
from db.models import StudentModel
from db.dto import *
from db.dao import student_dao, StudentDAO
from datetime import datetime
from loguru import logger


class StudentService:
    def __init__(self, student_dao: StudentDAO):
        self._student_dao = student_dao

    async def create(self, input_data: List[StudentCreateDTO]) -> dict:
        """checks if student is in the db AND is not deleted (deleted_at is None)
        if not -> makes a token for further user registration and creates a student
        returns both students failed to register and registered students
        if the student in the db and is not deleted - returns as failed to register"""
        logger.info(f"StudentService: Create students")
        logger.trace(f"StudentService: Register students with passed data {input_data}")
        students_to_create = []
        failed_creation = {}
        for student in input_data:
            logger.debug(f"StudentService: Check if student already exists in db and is not deleted: {student}")
            student.birth_date = datetime.strptime(student.birth_date, '%d-%m-%Y')
            in_db = await self._student_dao.get_all_by(**student.dict())
            active_students = [s for s in in_db if s.deleted_at is None]
            if active_students:
                logger.info(f"StudentService: Got existing student from db: {active_students}")
                notice = 'already exist in database'
                if notice in failed_creation:
                    failed_creation[notice].append(student)
                else:
                    failed_creation[notice] = [student]
            else:
                student.registration_token = secrets.token_urlsafe(10)
                students_to_create.append(student)
        logger.debug(f"StudentService: Students to be registered after check: {students_to_create}")
        resp = await self._student_dao.create(students_to_create)
        logger.debug(f"StudentService: Received the answer from database: {resp}")
        response = dict(failed_to_register=failed_creation, registered_students=resp)
        return response

    async def get_by(self, **kwargs) -> StudentModel:
        logger.info(f"StudentService: Get student by parameters: {kwargs}")
        response = await self._student_dao.get_by(**kwargs)
        return response

    async def get_all_by(self, *args, **kwargs) -> list:
        """gets all students who are not deleted (deleted_at is None) by arguments"""
        logger.info(f"StudentService: Get all not deleted students with given parameters")
        logger.trace(f"StudentService: Get all not deleted student with parameters: {kwargs}")
        resp = await self._student_dao.get_all_by(*args, **kwargs)
        response = [student for student in resp if student.deleted_at is None]
        return response

    async def get_by_id(self, user_id: str) -> StudentModel:
        logger.info(f"StudentService: Get student by id: {user_id}")
        response = await self._student_dao.get_by_id(user_id)
        if response is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Student with provided id does not exist.",
                                headers={"WWW-Authenticate": "Bearer"})
        return response

    async def set_registered(self, user_id: str, reg_flag: bool) -> NoReturn:
        logger.info(f"StudentService: Set student registered_user field")
        logger.trace(f"StudentService: Patch student with id: {user_id} - set registered_user: {reg_flag}")
        patch_data = StudentSetRegisteredDTO(
            registered_user=reg_flag
        )
        await self._student_dao.patch(patch_data, user_id)

    async def patch(self, user_id: str, patch_data: StudentPatchDTO) -> StudentModel:
        logger.info("StudentService: Update student")
        logger.trace(f"StudentService: Patch student with id: {user_id} - with following data: {patch_data}")
        resp = await self._student_dao.patch(patch_data, user_id)
        return resp

    async def delete(self, user_id: str) -> NoReturn:
        """sets deleted_at column value equal to utcnow time;
        doesn't remove raw from the table"""
        logger.info(f"StudentService: Delete student (mark student as deleted)")
        patch_data = StudentDeleteDTO(deleted_at=datetime.utcnow())
        logger.trace(f"StudentService: Patch student with id: {user_id} - with following data: {patch_data}")
        await self._student_dao.patch(patch_data, user_id)


student_service = StudentService(student_dao)
