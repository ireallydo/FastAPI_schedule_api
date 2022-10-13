from enum import Enum;

class ClassTypesEnum(str, Enum):
    LECTURE = 'лекция'
    SEMINAR = 'семинар'
    LABORATORY = 'лабораторная'
