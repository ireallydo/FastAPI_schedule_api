from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import group_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["group"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@cbv(router)
class GroupBusyView:
    db: Session = Depends(get_db)

    @router.post(ApiSpec.GROUP_BUSY, status_code=201, response_model=GroupBusyResponseDTO)
    def post_group_busy(self, input_data: GroupBusyRequestDTO):
        group_busy_db_entry = group_service.check_group_busy(self.db, input_data)
        if group_busy_db_entry:
            busy_flag=group_busy_db_entry.is_busy
            if busy_flag:
                raise HTTPException(status_code=400, detail=f'''Группа уже занята!''')
            else:
                group_service.set_group_busy(self.db, input_data)
        else:
            group_service.create_group_busy(self.db, input_data)
        response = group_service.check_group_busy(self.db, input_data)
        return response
