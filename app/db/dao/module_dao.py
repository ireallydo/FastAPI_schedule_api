from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.ModuleModel import ModuleModel
from db.enums import WeekdaysEnum
from db.dto import *
from .base_dao import BaseDAO


class ModuleDAO(BaseDAO[ModuleModel, ModuleCreateDTO, ModulePatchDTO, ModuleDeleteDTO]):

    def get_all_by_name(self, db: Session, module_name, skip, limit):
        response = db.query(self.model).filter(self.model.module_name==module_name).offset(skip).limit(limit).all()
        return response

module_dao = ModuleDAO(ModuleModel)
