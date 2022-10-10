from enum import Enum


class UserRoles(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
