from enum import Enum


class ApiSpec(str, Enum):
    SCHEDULE = '/schedule'
    SCHEDULE_MANUAL = '/schedule/manually'
    SCHEDULE_AUTO = '/schedule/auto'
    SCHEDULE_GROUP = '/schedule/semester_{semester}/group_{group}'
    SCHEDULE_TEACHER = '/schedule/semester_{semester}/teacher_{teacher_id}'

    MODULES = '/modules'
    GET_MODULES_BY_NAME = '/modules/{module_name}'
