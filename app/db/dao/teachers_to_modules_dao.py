from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.teachers_to_modules_association_table import teachers_to_modules_association
from db.dto import *
from .base_dao import BaseDAO


class TeachersToModulesDAO:
    def __init__(self, model):
        self.model = model

    def get_teachers_by_module(self, db, module_id):
        teachers_list = []
        response = db.query(self.model.teacher_id).where(self.model.modmodule_id==module_id).all()
        print(response)
        return teachers_list

teachers_to_modules_dao = TeachersToModulesDAO(teachers_to_modules_association)
