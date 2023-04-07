from typing import NoReturn, Any
from fastapi import HTTPException
from http import HTTPStatus
from db.models import LessonModel
from db.dto import LessonBaseDTO, LessonCreateDTO, LessonPatchDTO
from db.dao import lesson_dao, LessonDAO
from db.enums import LessonsEnum
from datetime import datetime
from loguru import logger


class LessonService:

    def __init__(self, lesson_dao: LessonDAO):
        self._lesson_dao = lesson_dao

    async def __convert_lesson_time(self, item: LessonBaseDTO) -> Any:
        item.start_time = datetime.strptime(item.start_time, '%H:%M').time()
        item.end_time = datetime.strptime(item.end_time, '%H:%M').time()
        return item

    async def __check_lesson_time(self, item: LessonBaseDTO) -> NoReturn:
        logger.debug(f"LessonService: Check if lesson within provided time scopes exists: {item.start_time} - {item.end_time}")
        in_db = await self._lesson_dao.get_same_time_scopes(item.start_time, item.end_time)
        if in_db:
            logger.info(f"LessonService: Got existing lesson from db: {r.dict() for r in in_db}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Lesson within provided time scopes already exists: {item.start_time} - {item.end_time}",
                                headers={"WWW-Authenticate": "Bearer"})

    async def create_lesson(self, item: LessonCreateDTO) -> LessonModel:
        """creates lesson if the lesson with the same number and within the same time scopes does not exist"""
        logger.info("LessonService: Create lesson")
        logger.trace(f"LessonService: Create lesson with passed data {item}")
        item = await self.__convert_lesson_time(item)
        logger.debug(f"LessonService: Check if lesson with same number exists: {item.lesson_number}")
        in_db = await self._lesson_dao.get_by(lesson_number=item.lesson_number)
        if in_db:
            logger.info(f"LessonService: Got existing lesson from db: {in_db}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Lesson with provided number already exists: {item.lesson_number}",
                                headers={"WWW-Authenticate": "Bearer"})
        await self.__check_lesson_time(item)
        response = await self._lesson_dao.create(item)
        return response

    async def get_all(self, *args) -> list:
        """gets all lessons"""
        logger.info("LessonService: Get all lessons")
        resp = await self._lesson_dao.get_all_by(*args)
        response = [lesson for lesson in resp]
        return response

    async def get_by_number(self, num: LessonsEnum) -> LessonModel:
        logger.info("LessonService: Get lesson by number")
        logger.trace(f"LessonService: Get lesson by number: {num}")
        response = await self._lesson_dao.get_by(lesson_number=num)
        if response is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="Lesson with provided number does not exist.",
                                headers={"WWW-Authenticate": "Bearer"})
        return response

    async def patch(self, num: LessonsEnum, patch_data: LessonPatchDTO) -> LessonModel:
        logger.info("LessonService: Patch lesson")
        logger.trace(f"LessonService: Patch lesson number: {num} with following data: {patch_data}")
        patch_data = await self.__convert_lesson_time(patch_data)
        await self.__check_lesson_time(patch_data)
        lesson = await self.get_by_number(num)
        resp = await self._lesson_dao.patch(patch_data, lesson.id)
        return resp

    async def delete(self, num: LessonsEnum) -> NoReturn:
        """deletes lesson from the database"""
        logger.info("LessonService: Delete lesson")
        lesson = await self.get_by_number(num)
        await self._lesson_dao.delete(lesson.id)


lesson_service = LessonService(lesson_dao)
