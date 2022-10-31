from enum import Enum

class UserRolesEnum(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
