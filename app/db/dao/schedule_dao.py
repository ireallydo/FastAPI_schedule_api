from db.models.ScheduleModel import ScheduleModel
from db.dto import ScheduleCreateDTO
from .base_dao import BaseDAO


class ScheduleDAO(BaseDAO[ScheduleModel, ScheduleCreateDTO, None, None]):
    pass


schedule_dao = ScheduleDAO(ScheduleModel)
