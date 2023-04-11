from db.models.TeacherBusyModel import TeacherBusyModel
from db.dto import TeacherBusyCreateDTO
from .base_dao import BaseDAO
from sqlalchemy import update, select
from loguru import logger


class TeacherBusyDAO(BaseDAO[TeacherBusyModel, TeacherBusyCreateDTO, None, None]):

    async def patch_busy(self, patch_data, teacher_id):
        logger.info("TeacherBusyDAO: Update db entry")
        logger.trace(
            f"TeacherBusyDAO: Data passed for update: item_id: {teacher_id}, patch_data: {patch_data}")
        async with self._session_generator() as session:
            await session.execute(update(self._model).
                                  filter(self._model.teacher_id == teacher_id,
                                         self._model.weekday == patch_data.weekday,
                                         self._model.lesson == patch_data.lesson).
                                  values(is_busy=patch_data.is_busy))
            await session.commit()
            resp = await session.execute(select(self._model).
                                         filter(self._model.teacher_id == teacher_id,
                                                self._model.weekday == patch_data.weekday,
                                                self._model.lesson == patch_data.lesson))
            resp = resp.scalar()
            logger.debug(f"TeacherBusyDAO: Received updated entry from the database")
            return resp


teacher_busy_dao = TeacherBusyDAO(TeacherBusyModel)
