from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import *
from db.dto import *
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


enum_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5};



# -----------------------------------------------------------------
# enum translation functions
# -----------------------------------------------------------------

def translate_enum_weekday(db: Session, weekday: WeekdaysEnum):
    '''is used to support mutilingual databases while using latin for input
    takes a value from the enum model as an input
    returns the matching weekday value from the 'weekdays' table in db
    e.g. "Monday" will return a proper weekday name from database in accordance with the enum attribute value'''
    if str(WeekdaysEnum(weekday).name) in enum_dict.keys():
        day_id=enum_dict[str(WeekdaysEnum(weekday).name)];
        db_weekday = db.query(WeekdayModel.name).where(WeekdayModel.id==day_id).all();
    return db_weekday[0][0];

def translate_enum_class_type(db: Session, class_type: ClassTypesEnum):
    '''is used to support mutilingual databases while using latin for input
    takes a class_type value from the enum model as an input
    returns the matching type of class value from the 'class_types' table in db
    e.g. "lecture" will return a proper class_type name from database in accordance with the enum attribute value'''
    if str(ClassTypesEnum(class_type).name) in enum_dict.keys():
        class_type_id=enum_dict[str(ClassTypesEnum(class_type).name)];
        db_class_type = db.query(TypeOfClassModel.name).where(TypeOfClassModel.id==class_type_id).all();
    return db_class_type[0][0];





#-----------------------------that's all, folks---------------------------------
