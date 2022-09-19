from enum import Enum;

class ClassTypesEnum(str, Enum):
    one = 'lecture';
    two = 'seminar';
    three = 'laboratory';
