from enum import Enum


class ApiSpec(str, Enum):
    USER = "/users"
    USER_INACTIVE = "/users/inactivity"
