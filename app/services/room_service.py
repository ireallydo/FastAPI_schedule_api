from typing import NoReturn, List
from http import HTTPStatus
from fastapi import HTTPException
from db.models import RoomModel, RoomBusyModel
from db.dto import RoomCreateDTO, RoomPatchDTO, RoomBusyRequestDTO, RoomBusyCreateDTO
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
                                detail="Room with provided number does not exist.",
                                headers={"WWW-Authenticate": "Bearer"})
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

    async def get_free_room(self, class_type, weekday, lesson, semester):
        """checks if there are free rooms of the provided class type, returns one"""
        rooms: List[RoomModel] = await self._room_dao.get_all_by(class_type=class_type)
        if not rooms:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail="There are no registered rooms to hold a class of provided type: {class_type}",
                                headers={"WWW-Authenticate": "Bearer"})
        for room in rooms:
            room_busy = await self.check_room_busy(room.id, weekday, lesson, semester)
            if room_busy is None or not room_busy.is_busy:
                return room

    async def check_room_busy(self, room_id, weekday, lesson, semester):
        room_busy = await self._room_busy_dao.get_by(
            room_id=room_id,
            weekday=weekday,
            lesson=lesson,
            semester=semester
        )
        return room_busy

    async def set_room_busy(self, num: int, input_data: RoomBusyRequestDTO) -> RoomBusyModel:
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



# def check_room_busy(db, room_id, weekday, lesson):
#     room_busy = room_busy_dao.check_busy(db, room_id, weekday, lesson)
#     return room_busy
#
# def get_spare_room(db, weekday, lesson):
#     spare_room = room_busy_dao.get_spare_room(db, weekday, lesson)
#     return spare_room.id
#
# def create_room_busy(db, room_id, weekday, lesson):
#     input_data = dict_of(room_id, weekday, lesson)
#     input_data["is_busy"]=True
#     room_busy_dao.create(db, input_data)
#     return check_room_busy(db, room_id, weekday, lesson)
#
# def set_room_busy(db, room_id, weekday, lesson):
#     room_busy_dao.set_busy(db, room_id, weekday, lesson)
#     return check_room_busy(db, room_id, weekday, lesson)
#
# def count_rooms_in_table(db):
#     count_busy = 0
#     for room in get_all_busy(db, 0, 100):
#         count_busy += 1
#     count_room = 0
#     for room in get_all(db, 0, 100):
#         count_room += 1
#     return count_busy < count_room
#
# def get_rooms_by_class_type(db, class_type):
#     result = room_dao.get_rooms_by_class_type(db, class_type)
#     return result


# def get_room_number_by_id(room_id: int):
#     '''takes a room id and returns correspondig room number'''
#     request_room_number = room_dao.get_by_id(room_id)
#     room_number = request_room_number[0][0]
#     return room_number

# def check_room_busy(db, room_id, weekday, lesson):
#
#     db_request = room_dao.check_busy(weekday, lesson)
#
#     return db_request.room_id
