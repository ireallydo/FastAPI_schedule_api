from enum import Enum


class ApiSpec(str, Enum):
    TEACHER = "/teachers"
    TEACHER_BUSY = "teacher_busy"
