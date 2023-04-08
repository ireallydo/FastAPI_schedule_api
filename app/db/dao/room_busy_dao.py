from sqlalchemy import update, select
from db.models.RoomBusyModel import RoomBusyModel
from db.dto import RoomBusyCreateDTO, RoomBusyRequestDTO
from .base_dao import BaseDAO
from loguru import logger


class RoomBusyDAO(BaseDAO[RoomBusyModel, RoomBusyCreateDTO, None, None]):

    async def patch_busy(self, patch_data: RoomBusyRequestDTO, room_id: str) -> RoomBusyModel:
        logger.info("RoomBusyDAO: Update db entry")
        logger.trace(
            f"RoomBusyDAO: Data passed for update: item_id: {room_id}, patch_data: {patch_data}")
        async with self._session_generator() as session:
            await session.execute(update(self._model).
                                  filter(self._model.room_id == room_id,
                                         self._model.weekday == patch_data.weekday,
                                         self._model.lesson == patch_data.lesson).
                                  values(is_busy=patch_data.is_busy))
            await session.commit()
            resp = await session.execute(select(self._model).
                                         filter(self._model.room_id == room_id,
                                                self._model.weekday == patch_data.weekday,
                                                self._model.lesson == patch_data.lesson))
            resp = resp.scalar()
            logger.debug(f"RoomBusyDAO: Received updated entry from the database")
            return resp


room_busy_dao = RoomBusyDAO(RoomBusyModel)
