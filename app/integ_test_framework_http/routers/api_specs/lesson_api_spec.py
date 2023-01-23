from enum import Enum


class ApiSpec(str, Enum):
    LESSON = "/lessons"
    LESSON_BY_NUMBER = "/lessons/{lesson_number}"
