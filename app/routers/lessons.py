from typing import List
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi_utils.cbv import cbv

from services import lesson_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["lessons"])

def get_db():
    db = SessionLocal()
    try:
        yield db;
    finally:
        db.close()

@cbv(router)
class LessonView:

    db: Session = Depends(get_db)

    @router.post(ApiSpec.LESSONS, status_code=HTTPStatus.CREATED, response_model=LessonDTO)
    def create_lesson(self, input_data: LessonCreateDTO):
        response = lesson_service.create_lesson(self.db, input_data)
        return response

    @router.get(ApiSpec.LESSONS, status_code=HTTPStatus.OK, response_model=List[LessonDTO])
    def get_all_lessons(self, skip: int = 0, limit=None):
        response = lesson_service.get_all(self.db, skip, limit)
        return response

    @router.get(ApiSpec.LESSONS_DETAILS, status_code=HTTPStatus.OK, response_model=LessonDTO)
    def get_lesson_by_number(self, lesson_number: LessonsEnum):
        response = lesson_service.get_by_number(self.db, lesson_number)
        return response

    @router.patch(ApiSpec.LESSONS_DETAILS, status_code=HTTPStatus.OK, response_model=LessonDTO)
    def patch_lesson(self, lesson_number: LessonsEnum, input_data: LessonPatchDTO):
        response = lesson_service.patch(self.db, lesson_number, input_data)
        return response

    @router.delete(ApiSpec.LESSONS_DETAILS, status_code=HTTPStatus.NO_CONTENT)
    def delete_lesson(self, lesson_number: LessonsEnum):
        lesson_service.delete(self.db, lesson_number)
        return Response(status_code=HTTPStatus.NO_CONTENT)
