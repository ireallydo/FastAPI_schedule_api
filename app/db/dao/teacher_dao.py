from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from fastapi import Depends, FastAPI, HTTPException

from db.models import UserModel

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

db: Session = Depends(get_db)

def set_busy(db: Session, teacher_id, weekday, lesson):
        db.query(TeacherBusyModel).filter(TeacherBusyModel.teacher_id==teacher_id,
                                                 TeacherBusyModel.weekday==weekday,
                                                 TeacherBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
        db.commit()

def get_id_by_module(db: Session, module_id):
    return db.query(teachers_to_modules).where(teachers_to_modules.c.Module_id==module_id).all()

def check_busy(db: Session, teacher_id, weekday, lesson):
    return db.query(TeacherBusyModel.is_busy).where(TeacherBusyModel.teacher_id==teacher_id,
                                                           TeacherBusyModel.weekday==weekday,
                                                           TeacherBusyModel.lesson==lesson).all()
