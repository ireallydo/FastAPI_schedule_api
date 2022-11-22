from sorcery import dict_of

from sqlalchemy.orm import Session
from sqlalchemy import select

from fastapi import Depends, FastAPI, HTTPException

from db.models.teachers_to_modules_association_table import teachers_to_modules_association
from db.models.ModuleModel import ModuleModel
from db.models.TeacherModel import TeacherModel
from db.dto import *
from .base_dao import BaseDAO


class TeachersToModulesDAO:
    def __init__(self, model):
        self.model = model

    def get_teachers_by_module(self, db, module_id):
        teachers_list = [row.teacher_id for row in db.query(self.model).filter(self.model.c.module_id==module_id).all()]
        print(teachers_list)
        return teachers_list

    def post_teacher_to_module(self, db, teacher_id, module_id):
        insert_cmd = self.model.insert().values(teacher_id=teacher_id, module_id=module_id)
        db.execute(insert_cmd)
        db.commit()

    def get_all(self, db):
        response = db.query(teachers_to_modules_association).all()
        return response

    def delete(self, db, module_id, teacher_id):
        db.query(self.model).filter(self.model.c.module_id==module_id, self.model.c.teacher_id==teacher_id).delete()
        db.commit()



teachers_to_modules_dao = TeachersToModulesDAO(teachers_to_modules_association)
