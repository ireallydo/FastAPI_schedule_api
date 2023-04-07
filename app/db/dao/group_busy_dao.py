from sqlalchemy import select, update
from db.models.GroupBusyModel import GroupBusyModel
from db.dto import GroupBusyCreateDTO, GroupBusyRequestDTO
from .base_dao import BaseDAO
from db.enums import AcademicGroupsEnum
from loguru import logger

class GroupBusyDAO(BaseDAO[GroupBusyModel, GroupBusyCreateDTO, None, None]):

    async def patch_busy(self, patch_data: GroupBusyRequestDTO, group_number: AcademicGroupsEnum) -> GroupBusyModel:
        logger.info("GroupBusyDAO: Update db entry")
        logger.trace(
            f"GroupBusyDAO: Data passed for update: group_number: {group_number}, patch_data: {patch_data}")
        async with self._session_generator() as session:
            await session.execute(update(self._model).
                                  filter(self._model.group_number == group_number,
                                         self._model.weekday == patch_data.weekday,
                                         self._model.lesson == patch_data.lesson).
                                  values(is_busy=patch_data.is_busy))
            await session.commit()
            resp = await session.execute(select(self._model).
                                         filter(self._model.group_number == group_number,
                                                self._model.weekday == patch_data.weekday,
                                                self._model.lesson == patch_data.lesson))
            resp = resp.scalar()
            logger.debug(f"GroupBusyDAO: Received updated entry from the database")
            return resp

group_busy_dao = GroupBusyDAO(GroupBusyModel)


# def set_busy(db: Session, group_id: int, weekday: str, lesson: int):
#     db.query(GroupBusyModel).filter(GroupBusyModel.group_id==group_id,
#                                              GroupBusyModel.weekday==weekday,
#                                              GroupBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
#     db.commit();
#
# def check_busy(db:Session, group_number: int, weekday: WeekdaysEnum, lesson_number: int):
#     return db.query(GroupBusyModel.is_busy).where(GroupBusyModel.group_id==group_id,
#                                                            GroupBusyModel.weekday==db_weekday,
#                                                            GroupBusyModel.lesson==lesson_number).all();
#
#
# #group_dao = GroupDao()
