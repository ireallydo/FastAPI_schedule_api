from enum import Enum


class ApiSpec(str, Enum):

    AUTH = '/login'
    AUTH_USER = '/me'

    USERS = '/users'
    USERS_DETAILES = '/users/{user_id}'
    USERS_PASSWORD ='/users/{user_id}/change_password'
    USERS_BLOCK = '/users/{user_id}/blocked'

    STUDENTS = '/students'
    STUDENTS_DETAIL = '/students/{user_id}'
    STUDENTS_BY_GROUP = '/students/group/{group_number}'
    STUDENTS_BY_YEAR = '/students/year/{year_number}'

    TEACHERS = '/teachers'
    TEACHERS_DETAIL = '/teachers/{user_id}'
    TEACHERS_BUSY = '/teachers/{user_id}/busy'
    TEACHERS_MODULES = '/teachers/{user_id}/modules'

    MODULES = '/modules'
    MODULES_DETAILS = '/modules/{module_id}'
    MODULES_TEACHERS = '/modules/{module_id}/teachers'

    LESSONS = '/lessons'
    LESSONS_DETAILS = '/lessons/{lesson_number}'

    ROOMS = '/rooms'
    ROOMS_DETAILS = '/rooms/{room_number}'
    ROOMS_BUSY = '/rooms/{room_number}/busy'

    SCHEDULE = '/schedule'
    SCHEDULE_MANUAL = '/schedule/manually'
    SCHEDULE_AUTO = '/schedule'
    SCHEDULE_GROUP = '/schedule/semester_{semester}/group_{group}'
    SCHEDULE_TEACHER = '/schedule/semester_{semester}/teacher_{teacher_id}'


    GROUP_BUSY = '/group_busy'
