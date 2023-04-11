from typing import NoReturn, List, Union
from uuid import UUID
from http import HTTPStatus
from fastapi import HTTPException
from db.enums import LessonsEnum, SemestersEnum, WeekdaysEnum, ClassTypesEnum
from db.models import RoomModel, RoomBusyModel
from db.dto import RoomCreateDTO, RoomPatchDTO, RoomBusyRequestDTO, RoomBusyCreateDTO, BusyDTO
from db.dao import room_dao, RoomDAO, room_busy_dao, RoomBusyDAO
from loguru import logger


class RoomService:

    def __init__(self, room_dao: RoomDAO, room_busy_dao: RoomBusyDAO):
        self._room_dao = room_dao
        self._room_busy_dao = room_busy_dao

    async def create_room(self, item: RoomCreateDTO) -> RoomModel:
        """creates a room if a room with the same number does not exist"""
        logger.info("RoomService: Create room")
        logger.trace(f"RoomService: Create room with passed data {item}")
        logger.debug(f"RoomService: Check if room with same number exists: {item.room_number}")
        in_db = await self._room_dao.get_by(room_number=item.room_number)
        if in_db:
            logger.info(f"RoomService: Got existing room from db: {in_db}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"Room with provided number already exists: {item.room_number}",
                                headers={"WWW-Authenticate": "Bearer"})
        response = await self._room_dao.create(item)
        return response

    async def get_all(self, *args) -> list:
        logger.info("RoomService: Get all rooms")
        resp = await self._room_dao.get_all_by(*args)
        response = [room for room in resp]
        return response

    async def get_by_number(self, num: int) -> RoomModel:
        logger.info("RoomService: Get room by number")
        logger.trace(f"RoomService: Get room by number: {num}")
        response = await self._room_dao.get_by(room_number=num)
        if response is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="Room with provided number does not exist.")
        return response

    async def patch(self, num: int, patch_data: RoomPatchDTO) -> RoomModel:
        logger.info("RoomService: Patch room")
        logger.trace(f"RoomService: Patch room number: {num} with following data: {patch_data}")
        room = await self.get_by_number(num)
        resp = await self._room_dao.patch(patch_data, room.id)
        return resp

    async def delete(self, num: int) -> NoReturn:
        """deletes room from the database"""
        logger.info("RoomService: Delete room")
        room = await self.get_by_number(num)
        await self._room_dao.delete(room.id)

    async def get_free_room(self, class_type: ClassTypesEnum, weekday: WeekdaysEnum,
                            lesson: LessonsEnum, semester: SemestersEnum) -> Union[RoomModel, NoReturn]:
        """checks if there are free rooms of the provided class type, returns one"""
        logger.info("RoomService: Get free room")
        rooms: List[RoomModel] = await self._room_dao.get_all_by(class_type=class_type)
        if not rooms:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="There are no registered rooms to hold a class of provided type: {class_type}")
        for room in rooms:
            room_busy = await self.check_room_busy(room.id, weekday, lesson, semester)
            if room_busy is None or not room_busy.is_busy:
                return room

    async def check_room_busy(self, room_id: Union[str, UUID], weekday: WeekdaysEnum,
                              lesson: LessonsEnum, semester: SemestersEnum) -> RoomBusyModel:
        logger.info("RoomService: Check room busy")
        room_busy = await self._room_busy_dao.get_by(
            room_id=room_id,
            weekday=weekday,
            lesson=lesson,
            semester=semester
        )
        return room_busy

    async def set_room_busy(self, num: int, input_data: Union[BusyDTO, RoomBusyRequestDTO]) -> RoomBusyModel:
        logger.info("RoomService: Set room busy")
        logger.trace(f"RoomService: Set room busy: room_number: {num}, data: {input_data}")
        room = await self.get_by_number(num)
        room_busy = await self.check_room_busy(room.id, input_data.weekday, input_data.lesson, input_data.semester)
        if room_busy is None:
            obj = RoomBusyCreateDTO(
                room_id=room.id,
                weekday=input_data.weekday,
                lesson=input_data.lesson,
                semester=input_data.semester,
                is_busy=input_data.is_busy
            )
            response = await self._room_busy_dao.create(obj)
        else:
            try:
                assert (room_busy.is_busy != input_data.is_busy)
                response = await self._room_busy_dao.patch_busy(input_data, room.id)
            except AssertionError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail=f"The room is already set busy: {input_data.is_busy} at this time.")
        return response


room_service = RoomService(room_dao, room_busy_dao)
