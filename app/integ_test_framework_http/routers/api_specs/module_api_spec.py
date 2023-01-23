from enum import Enum


class ApiSpec(str, Enum):
    MODULE = "/modules"
    MODULE_BY_NAME = "/modules/{module_name}"
