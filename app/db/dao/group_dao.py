from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import UserModel

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

db: Session = Depends(get_db)

#class GroupDao:

# def get_id_by_number(db: Session, group: int):
#     return db.query(AcademicGroupModel.id).where(AcademicGroupModel.number==group)

def set_busy(db: Session, group_id: int, weekday: str, lesson: int):
    db.query(GroupBusyModel).filter(GroupBusyModel.group_id==group_id,
                                             GroupBusyModel.weekday==weekday,
                                             GroupBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
    db.commit();

def check_busy(db:Session, group_number: int, weekday: WeekdaysEnum, lesson_number: int):
    return db.query(GroupBusyModel.is_busy).where(GroupBusyModel.group_id==group_id,
                                                           GroupBusyModel.weekday==db_weekday,
                                                           GroupBusyModel.lesson==lesson_number).all();


#group_dao = GroupDao()
