from typing import List, NoReturn, Union
from uuid import UUID
from http import HTTPStatus
from fastapi import HTTPException
from datetime import datetime
import secrets
from db.enums import LessonsEnum, SemestersEnum, WeekdaysEnum
from db.models import TeacherModel, ModuleModel, TeacherBusyModel
from db.dto import TeacherCreateDTO, TeacherDeleteDTO, TeacherWithModulesDTO,\
    TeacherBusyCreateDTO, TeacherSetRegisteredDTO, BusyDTO, TeacherBusyRequestDTO
from db.dao import teacher_dao, TeacherDAO, teacher_busy_dao, TeacherBusyDAO
from loguru import logger


class TeacherService:

    def __init__(self, teacher_dao: TeacherDAO, teacher_busy_dao: TeacherBusyDAO):
        self._teacher_dao = teacher_dao
        self._teacher_busy_dao = teacher_busy_dao

    async def create(self, input_data: List[TeacherCreateDTO]) -> dict:
        """checks if teacher is in the db AND is not deleted (deleted_at is None)
        if not -> makes a token for further user registration and creates a teacher
        returns both teachers failed to register and registered teachers
        if the teacher in the db and is not deleted - returns as failed to register"""
        logger.info("TeacherService: Create teachers")
        logger.trace(f"TeacherService: Register teachers with passed data {input_data}")
        teachers_to_create = []
        failed_creation = {}
        for teacher in input_data:
            logger.debug(f"TeacherService: Check if teacher already exists in db and is not deleted: {teacher}")
            teacher.birth_date = datetime.strptime(teacher.birth_date, '%d-%m-%Y')
            in_db = await self._teacher_dao.get_all_by(**teacher.dict())
            active_teachers = [t for t in in_db if t.deleted_at is None]
            if active_teachers:
                logger.info(f"TeacherService: Got existing teacher from db: {active_teachers}")
                notice = 'already exist in database'
                if notice in failed_creation:
                    failed_creation[notice].append(teacher)
                else:
                    failed_creation[notice] = [teacher]
            else:
                teacher.registration_token = secrets.token_urlsafe(10)
                teachers_to_create.append(teacher)
        logger.debug(f"TeacherService: Teachers to be registered after check: {teachers_to_create}")
        resp = await self._teacher_dao.create(teachers_to_create)
        logger.debug(f"TeacherService: Received the answer from database: {resp}")
        response = dict(failed_to_register=failed_creation, registered_teachers=resp)
        return response

    async def set_registered(self, user_id: str, reg_flag: bool) -> NoReturn:
        logger.info("TeacherService: Set teacher registered_user field")
        logger.trace(f"TeacherService: Patch teacher with id: {user_id} - set registered_user: {reg_flag}")
        patch_data = TeacherSetRegisteredDTO(
            registered_user=reg_flag
        )
        await self._teacher_dao.patch(patch_data, user_id)

    async def get_all(self, *args) -> list:
        """gets all teachers who are not deleted (deleted_at is None)"""
        logger.info("TeacherService: Get all not deleted teachers")
        resp = await self._teacher_dao.get_all_by(*args)
        response = [teacher for teacher in resp if teacher.deleted_at is None]
        return response

    async def get_by_id(self, user_id: str) -> TeacherModel:
        logger.info(f"TeacherService: Get teacher by id: {user_id}")
        return await self._teacher_dao.get_by_id(user_id)

    async def delete(self, user_id: str) -> NoReturn:
        """sets deleted_at column value equal to utcnow time;
        doesn't remove raw from the table"""
        logger.info("TeacherService: Delete teacher (mark student as deleted)")
        patch_data = TeacherDeleteDTO(deleted_at=datetime.utcnow())
        logger.trace(f"TeacherService: Patch teacher with id: {user_id} - with following data: {patch_data}")
        await self._teacher_dao.patch(patch_data, user_id)

    async def create_teacher_modules(self, user_id: str, modules: list) -> TeacherWithModulesDTO:
        """adds modules that are not in teacher modules to teacher modules"""
        logger.info("TeacherService: Create teacher modules")
        logger.trace(f"TeacherService: Create teacher modules: teacher_id: {user_id}")
        teacher = await self.get_by_id(user_id)
        mod_ids = [module.id for module in teacher.modules]
        modules_to_add = []
        for module in modules:
            if module.id not in mod_ids:
                logger.trace(f"TeacherService: Module {module.id} will be added to teacher's modules.")
                modules_to_add.append(module)
            else:
                logger.trace(f"TeacherService: Module {module.id} is already in teacher's modules.")
        modules_response = await self._teacher_dao.create_modules(user_id, modules_to_add)
        resp = TeacherWithModulesDTO(
            teacher_id=user_id,
            modules=modules_response
        )
        return resp

    async def get_modules(self, user_id: str) -> list:
        logger.info("TeacherService: Get teacher modules")
        logger.trace(f"TeacherService: Get teacher modules: teacher_id: {user_id}")
        teacher = await self.get_by_id(user_id)
        modules = teacher.modules
        return modules

    async def delete_teacher_module(self, user_id, module: ModuleModel) -> NoReturn:
        logger.info("TeacherService: Delete teacher module")
        logger.trace(f"TeacherService: Delete teacher modules: teacher_id: {user_id}, module_id: {module.id}")
        await self._teacher_dao.delete_teacher_module(user_id, module)

    async def check_teacher_busy(self, user_id: Union[str, UUID], weekday: WeekdaysEnum,
                                 lesson: LessonsEnum, semester: SemestersEnum) -> TeacherBusyModel:
        teacher_busy = await self._teacher_busy_dao.get_by(
            teacher_id=user_id,
            weekday=weekday,
            lesson=lesson,
            semester=semester
        )
        return teacher_busy

    async def set_teacher_busy(self, user_id: Union[str, UUID],
                               input_data: Union[BusyDTO, TeacherBusyRequestDTO]) -> TeacherBusyModel:
        logger.info("TeacherService: Set teacher busy")
        logger.trace(f"TeacherService: Set teacher busy: teacher_id: {user_id}, data: {input_data}")
        teacher_busy = await self.check_teacher_busy(user_id, input_data.weekday, input_data.lesson, input_data.semester)
        if teacher_busy is None:
            obj = TeacherBusyCreateDTO(
                teacher_id=user_id,
                weekday=input_data.weekday,
                lesson=input_data.lesson,
                semester=input_data.semester,
                is_busy=input_data.is_busy
            )
            response = await self._teacher_busy_dao.create(obj)
        else:
            try:
                assert (teacher_busy.is_busy != input_data.is_busy)
                response = await self._teacher_busy_dao.patch_busy(input_data, user_id)
            except AssertionError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail=f"The teacher is already set busy: {input_data.is_busy} at this time.")
        return response


teacher_service = TeacherService(teacher_dao, teacher_busy_dao)
