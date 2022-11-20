from enum import Enum


class ApiSpec(str, Enum):
    SCHEDULE = '/schedule'
    SCHEDULE_MANUAL = '/schedule/manually'
    SCHEDULE_AUTO = '/schedule/auto'
    SCHEDULE_GROUP = '/schedule/semester_{semester}/group_{group}'
    SCHEDULE_TEACHER = '/schedule/semester_{semester}/teacher_{teacher_id}'

    MODULES = '/modules'
    GET_MODULES_BY_NAME = '/modules/{module_name}'

    TEACHERS = '/teachers'
    TEACHER_BUSY = '/teacher_busy'

    STUDENTS = '/students'
    GET_STUDENT_BY_NAME = '/students/name/{first_name}/surname/{last_name}'
    GET_STUDENTS_BY_GROUP = '/students/group/{group_number}'
    GET_STUDENTS_BY_YEAR = '/students/year/{year_number}'

    GROUP_BUSY = '/group_busy'

    LESSONS = '/lessons'
    GET_LESSON_TIME_BY_NUMBER = '/lessons/{lesson_number}'

    ROOMS = '/rooms'
    ROOM_BUSY = '/room_busy'
    GET_ROOM_CLASSTYPE_BY_NUMBER = '/rooms/{room_number}'

    USERS = '/users'
    USERS_INACTIVE = '/users/inactivity'

    AUTH = '/login'
    AUTH_USER = '/me'
