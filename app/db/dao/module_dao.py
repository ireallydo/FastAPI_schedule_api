from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.ModuleModel import ModuleModel
from db.enums import WeekdaysEnum
from db.dto import *
from .base_dao import BaseDAO


class ModuleDAO(BaseDAO[ModuleModel, ModuleCreateDTO, None, None]):

    def get_teachers(self, db, module_id):
        return db.query(self.model).where(id=module_id).join(self.model.teachers).all()


module_dao = ModuleDAO(ModuleModel)
