from typing import List

from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import lesson_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["lesson"])

def get_db():
    db = SessionLocal()
    try:
        yield db;
    finally:
        db.close()

@cbv(router)
class LessonView:

    db: Session = Depends(get_db)

    @router.post(ApiSpec.LESSONS, status_code=201, response_model=LessonDTO)
    def post_lesson(self, input_data: LessonCreateDTO):
        response = lesson_service.create(self.db, input_data)
        return response

    @router.get(ApiSpec.LESSONS, status_code=200, response_model=List[LessonDTO])
    def get_lessons(self, skip: int = 0, limit: int = 100):
        response = lesson_service.get_all(self.db, skip=skip, limit=limit)
        return response

    @router.get(ApiSpec.GET_LESSON_TIME_BY_NUMBER, status_code=200, response_model=LessonDTO)
    def get_lesson_time_by_number(self, lesson_number: LessonsEnum):
        response = lesson_service.get_time_by_number(self.db, lesson_number)
        return response

    @router.patch(ApiSpec.LESSONS, status_code=201, response_model=LessonDTO)
    def patch_lesson(self, search_data: LessonSearchDTO, patch_data: LessonPatchDTO):
        response = lesson_service.patch(self.db, search_data, patch_data)
        return response

    @router.delete(ApiSpec.LESSONS, responses={200: {'model': str}})
    def delete_lesson(self, input_data: LessonDeleteDTO):
        lesson_service.delete(self.db, input_data)
        return JSONResponse(status_code=200, content={'message': f'Урок № {input_data.lesson_number} был успешно удален из базы данных!'})
