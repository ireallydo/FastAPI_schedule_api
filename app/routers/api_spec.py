from enum import Enum


class ApiSpec(str, Enum):

    AUTH = '/login'
    REGISTRATION = '/register'

    USERS = '/users'
    USERS_DETAILS = '/users/{user_id}'
    USERS_RESTORE = '/users/{user_id}/restore'
    USERS_PASSWORD = '/users/{user_id}/change_password'
    USERS_BLOCK = '/users/{user_id}/blocked'

    STUDENTS = '/students'
    STUDENTS_DETAILS = '/students/{user_id}'
    STUDENTS_BY_GROUP = '/students/group/{group_number}'
    STUDENTS_BY_YEAR = '/students/year/{year_number}'

    TEACHERS = '/teachers'
    TEACHERS_DETAILS = '/teachers/{user_id}'
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
    SCHEDULE_GROUP = '/schedule/{semester}/group/{group_number}'
    SCHEDULE_TEACHER = '/schedule/{semester}/teacher/{teacher_id}'
    DELETE_SCHEDULE = '/schedule/{schedule_id}'
    CLEAR_SCHEDULE = '/schedule/semester/{semester}'

    GROUP_BUSY = '/groups/{group_number}/busy'
