from enum import Enum


class ApiSpec(str, Enum):
    STUDENT = "/students"
    STUDENT_BY_NAME = "/students/name/{first_name}/surname/{last_name}"
    STUDENTS_BY_GROUP = "/students/group/{group_number}"
    STUDENTS_BY_YEAR = "/students/year/{year_number}"
