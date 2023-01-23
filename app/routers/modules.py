from typing import List
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from fastapi_utils.cbv import cbv

from services import module_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["modules"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class ModuleView:
    # dependencies as class attributes
    db: Session = Depends(get_db)

    @router.post(ApiSpec.MODULES, status_code=HTTPStatus.CREATED, response_model=ModuleDTO)
    def create_module(self, input_data: ModuleCreateDTO):
        response = module_service.create_module(self.db, input_data)
        return response

    @router.get(ApiSpec.MODULES, status_code=HTTPStatus.OK, response_model=List[ModuleDTO])
    def get_all_modules(self, skip: int = 0, limit=None):
        response = module_service.get_all_modules(self.db, skip, limit)
        return response

    @router.get(ApiSpec.MODULES_DETAILS, status_code=HTTPStatus.OK, response_model=ModuleDTO)
    def get_module_by_id(self, module_id):
        response = module_service.get_by_id(self.db, module_id)
        return response

    @router.get(ApiSpec.MODULES_TEACHERS, status_code=HTTPStatus.OK, response_model=ModuleTeachersDTO)
    def get_module_teachers(self, module_id):
        response = module_service.get_teachers(self.db, module_id)
        return response

    @router.delete(ApiSpec.MODULES_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    def delete_module(self, module_id):
        module_service.delete(self.db, module_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)
