from enum import Enum


class ApiSpec(str, Enum):
    ROOM = "/rooms"
    ROOM_BY_NUMBER = "/rooms/{room_number}"
    ROOM_BUSY = "/room_busy"
