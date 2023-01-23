from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;
from sorcery import dict_of

from db.models import *
from db.dto import *
from db.dao import room_dao, room_busy_dao
from db.enums import ClassTypesEnum


def create_room(db, input_data):
    return room_dao.create(db, input_data)

def get_all(db, skip, limit):
    return room_dao.get_all_by(db, skip, limit)

def get_all_busy(db, skip, limit):
    return room_busy_dao.get_all_by(db, skip, limit)

def patch(db, room_number, input_data):
    room = get_by_number(db, room_number)
    room_dao.patch(db, input_data, room.id)
    return get_by_number(db, room_number)

def delete(db, room_number):
    room = get_by_number(db, room_number)
    return room_dao.delete(db, room.id)

def get_by_number(db, room_number):
    return room_dao.get_room_by_number(db, room_number)

def set_room_busy(db, room_number, input_data):
    room = get_by_number(db, room_number)
    print(room.id)
    check_data = dict_of(room_id=room.id)
    check_data.update(input_data.dict())
    print(check_data)
    room_busy = room_busy_dao.get_by(db, check_data)
    if room_busy != None:
        try:
            assert (room_busy.is_busy != input_data.is_busy)
            patch_data = [(k, v) for k, v in input_data.dict().items()]
            room_busy_dao.patch(db, patch_data, room.id)
        except AssertionError:
            raise HTTPException(status_code=404, detail="The room already has the provided busy status at this time.")
    else:
        input_data.dict().update(room_id=room.id)
        room = room_busy_dao.create(db, input_data)
    return get_by_number(db, room_number)





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
