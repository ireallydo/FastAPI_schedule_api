from sqlalchemy import select, or_, and_
from fastapi import Depends, FastAPI, HTTPException

from db.models.LessonModel import LessonModel
from db.enums import LessonsEnum
from db.dto import *
from .base_dao import BaseDAO
from loguru import logger


class LessonDAO(BaseDAO[LessonModel, LessonCreateDTO, LessonPatchDTO, LessonDeleteDTO]):

    async def get_same_time_scopes(self, start_time, end_time) -> list:
        logger.info("LessonDAO: Get lessons within same time scopes")
        logger.trace(
            f"LessonDAO: Get db entries within provided time scopes: {start_time} - {end_time}")
        async with self._session_generator() as session:
            result = await session.execute(select(self._model).where(or_(and_(self._model.start_time >= start_time,
                                                                          self._model.start_time <= end_time),
                                                                         and_(self._model.end_time >= start_time,
                                                                          self._model.end_time <= end_time))))
        resp = [raw[0] for raw in result]
        logger.debug(f"LessonDAO: received a response from the database {resp}")
        return resp

lesson_dao = LessonDAO(LessonModel)
