from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import module_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["module"])

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

    @router.post(ApiSpec.MODULES, status_code=201, response_model=ModuleDTO)
    def post_module(self, input_data: ModuleCreateDTO):
        response = module_service.fill(self.db, input_data)
        return response

    @router.get(ApiSpec.MODULES, status_code=200, response_model=List[ModuleDTO])
    def get_modules(self, skip: int = 0, limit: int = 100):
        response = module_service.get_all(self.db, skip=skip, limit=limit)
        return response

    @router.get(ApiSpec.GET_MODULES_BY_NAME, status_code=200, response_model=List[ModuleDTO])
    def get_modules_by_name(self, module_name: str, skip: int = 0, limit: int = 100):
        response = module_service.get_by_name(self.db, module_name, skip, limit)
        return response

    @router.patch(ApiSpec.MODULES, status_code=201, response_model=ModuleDTO)
    def patch_module(self, search_data: ModuleCreateDTO, patch_data: ModulePatchDTO):
        response = module_service.patch(self.db, search_data, patch_data)
        return response

    @router.delete(ApiSpec.MODULES, responses={200: {'model': str}})
    def delete_module(self, input_data: ModuleDeleteDTO):
        module_service.delete(self.db, input_data)
        return JSONResponse(status_code=200, content={'message': f'Предмет {input_data.module_name} ({input_data.class_type}) для {input_data.academic_year} академического года был успешно удален из базы данных!'})
