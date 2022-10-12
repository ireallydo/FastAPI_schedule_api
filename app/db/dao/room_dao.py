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

def get_by_id(db: Session, room_id):
    return db.query(RoomModel.number).where(RoomModel.id==room_id)

def check_busy(db: Session, weekday, lesson):
    return db.query(RoomBusyModel).where(RoomBusyModel.weekday==weekday,
                                                 RoomBusyModel.lesson==lesson,
                                                 RoomBusyModel.is_busy==False).first()
