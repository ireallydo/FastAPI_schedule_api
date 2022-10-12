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

#class UserDao:

def get_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_by_email(db:Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session, skip: int, limit: int):
    return db.query(UserModel).offset(skip).limit(limit).all()

#user_dao = UserDao()
