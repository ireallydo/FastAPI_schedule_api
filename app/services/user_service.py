from db.models import *
from db.dto import *
from db.dao import user_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum

# -----------------------------------------------------------------
# auth functions
# -----------------------------------------------------------------

def get_user_by_id(user_id: int):
    return user_dao.get_by_id(db=db, user_id=user_id)

def get_user_by_email(email:str):
    return user_dao.get_by_email(db=db, email=email)

def get_users(skip: int = 0, limit: int = 100):
    return user_dao.get_(db=db, skip=0, int=100)
