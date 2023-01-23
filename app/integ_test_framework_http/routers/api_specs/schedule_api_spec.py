from enum import Enum


class ApiSpec(str, Enum):
    SCHEDULE = "/schedule"
    SCHEDULE_MANUALLY = "/schedule/manually"
    SCHEDULE_GROUP = "/schedule/semester_{semester}/group_{group}"
    SCHEDULE_TEACHER = "schedule/semester_{semester}/teacher_{teacher_id}"
