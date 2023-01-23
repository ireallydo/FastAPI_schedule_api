from enum import Enum


class ApiSpec(str, Enum):
    LOGIN = "/login"
    GET_ME = "/me"
