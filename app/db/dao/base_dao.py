from pydantic import BaseModel as BaseSchema
from sqlalchemy import select, update
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from typing import Generic, TypeVar, Type, Optional, Any, List, Union
from uuid import UUID

from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models import BaseModel, TeacherModel
from db.enums import WeekdaysEnum
from db.dto import *


DBModelType = TypeVar("DBModelType", bound=BaseModel)
CreateDTOType = TypeVar("CreateDTOType", bound=BaseSchema)
UpdateDTOType = TypeVar("UpdateDTOType", bound=BaseSchema)
DeleteDTOType = TypeVar("DeleteDTOType", bound=BaseSchema)

class BaseDAO(Generic[DBModelType, CreateDTOType, UpdateDTOType, DeleteDTOType]):
    def __init__(self, model: Type[DBModelType]):
        self.model = model

    def create(self, db: Session, input_data: CreateDTOType):
        db_model = self.model
        if type(input_data) is dict:
            new_line = self.model(**input_data)
        else:
            new_line = self.model(**input_data.dict())
        db.add(new_line)
        db.commit()
        db.refresh(new_line)
        print(new_line)
        return new_line

    def get_all(self, db: Session, skip: int, limit: int):
        db_model = self.model
        response =  db.query(db_model).offset(skip).limit(limit).all()
        return response

    def get_by_id(self, db: Session, id):
        result = db.query(self.model).filter(self.model.id==id).one()
        return result

    def get_by(self, db: Session, input_data):
        if type(input_data) is dict:
            db_item = db.query(self.model).filter_by(**input_data).first()
        else:
            db_item = db.query(self.model).filter_by(**input_data.dict()).first()
        return db_item

    def delete(self, db: Session, id: UUID):
        db_model = self.model
        db.query(db_model).filter(db_model.id==id).delete()
        db.commit()

    def patch(self, db: Session, patch_data, id):
        update_dict=patch_data.dict()
        update_obj = []
        update_keys = update_dict.keys()
        for key in update_keys:
            print(key)
            update_obj.append((getattr(self.model, key), update_dict[key]))
        db.query(self.model).filter(self.model.id==id).update(update_obj,
        update_args={'preserve_parameter_order': True})
        db.commit()
