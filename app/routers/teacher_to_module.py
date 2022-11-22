from typing import List, Union

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import student_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["teacher_to_module"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class teacherToModuleView:

    db: Session = Depends(get_db)

    @router.post(ApiSpec.TEACHERS_MODULES, status_code=200, response_model=TeachersToModulesDTO)
    def post_teacher_to_module(self, input_data: TeachersToModulesCreateDTO):
        return teacher_to_module_service.post_teacher_to_module(self.db, input_data)

    @router.get(ApiSpec.TEACHERS_MODULES, status_code=200, response_model=TeachersToModulesDTO)
    def get_teachers_to_modules(self, input_data: TeachersToModulesGetDTO):
        return teacher_to_module_service.get_by_input(self.db, input_data)

    @router.patch(ApiSpec.TEACHERS_MODULES, status_code=200, response_model=TeachersToModulesDTO)
    def patch_teacher_to_module(self, input_data: TeachersToModulesPatchDTO):
        return teacher_to_module_service.patch_teacher_to_module(self.db, input_data)

    @router.delete(ApiSpec.TEACHERS_MODULES, status_code=201)
    def delete_teacher_to_module(self, input_data: TeachersToModulesDeleteDTO):
        return teacher_to_module_service.delete_teacher_to_module(self.db, input_data)
