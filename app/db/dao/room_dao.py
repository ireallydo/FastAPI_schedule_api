from db.models.RoomModel import RoomModel
from db.dto import RoomCreateDTO, RoomPatchDTO
from .base_dao import BaseDAO


class RoomDAO(BaseDAO[RoomModel, RoomCreateDTO, RoomPatchDTO, None]):
    pass


room_dao = RoomDAO(RoomModel)
