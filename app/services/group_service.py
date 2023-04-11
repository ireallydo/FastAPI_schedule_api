from typing import Union
from http import HTTPStatus
from fastapi import HTTPException
from db.models import GroupBusyModel
from db.dto import GroupBusyRequestDTO, GroupBusyCreateDTO, BusyDTO
from db.dao import group_busy_dao, GroupBusyDAO
from db.enums import AcademicGroupsEnum, WeekdaysEnum, LessonsEnum, SemestersEnum
from loguru import logger


class GroupService:

    def __init__(self, group_busy_dao: GroupBusyDAO):
        self._group_busy_dao = group_busy_dao

    async def check_group_busy(self, num: AcademicGroupsEnum, weekday: WeekdaysEnum,
                               lesson: LessonsEnum, semester: SemestersEnum) -> Union[GroupBusyModel, None]:
        logger.info("GroupService: Check group busy")
        group_busy = await self._group_busy_dao.get_by(
            group_number=num,
            weekday=weekday,
            lesson=lesson,
            semester=semester
        )
        return group_busy

    async def set_group_busy(self, num: AcademicGroupsEnum,
                             input_data: Union[BusyDTO, GroupBusyRequestDTO]) -> GroupBusyModel:
        logger.info("GroupService: Set group busy")
        logger.trace(f"GroupService: Set group busy: group_number: {num}, data: {input_data}")
        group_busy = await self.check_group_busy(num, input_data.weekday, input_data.lesson, input_data.semester)
        if group_busy is None:
            obj = GroupBusyCreateDTO(
                group_number=num,
                weekday=input_data.weekday,
                lesson=input_data.lesson,
                semester=input_data.semester,
                is_busy=input_data.is_busy
            )
            response = await self._group_busy_dao.create(obj)
        else:
            try:
                assert (group_busy.is_busy != input_data.is_busy)
                response = await self._group_busy_dao.patch_busy(input_data, num)
            except AssertionError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail=f"The group is already set busy: {input_data.is_busy} at this time.")
        return response


group_service = GroupService(group_busy_dao)
