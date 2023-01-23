from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from db.models.TeacherModel import TeacherModel
from db.dto import *
from .base_dao import BaseDAO


class TeacherDAO(BaseDAO[TeacherModel, TeacherCreateDTO, None, None]):

    def get_by_login(self, db, login):
        return db.query(TeacherModel).where(TeacherModel.login==login).all()

    def create_modules(self, db, user_id, modules):
        teacher = db.query(self.model).where(self.model.id==user_id).first()
        teacher.modules = [module_id for module_id in modules]
        db.commit()

    def get_modules(self, db, user_id):
        modules = db.query(self.model).where(self.model.id==user_id).join(self.model.modules).all()
        return modules

    # def get_modules(self, db, user_id):
    #     return db.query(self.model.modules).where(self.model.id==user_id).all()

    def delete_module(self, db, user_id, module_id):
        db.query(self.model.modules).filter(self.model.id==user_id, self.model.modules.id==module_id).delete()
        db.commit()



teacher_dao = TeacherDAO(TeacherModel)
