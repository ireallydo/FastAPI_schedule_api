from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import group_service, room_service, schedule_service, teacher_service, user_service

from db.models import *
from db.dto import *
from db.enums import *
from .api_spec import ApiSpec

from db.database import SessionLocal, engine


router = APIRouter(tags=["schedule"])

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

#----------------------------
# CREATE endpoints (additional endpoints for admins - downpage)
#----------------------------

@cbv(router)
class ScheduleView:
    # dependencies as class attributes
    db: Session = Depends(get_db)

    #admins only
    @router.post(ApiSpec.SCHEDULE_MANUAL, status_code=201, response_model=ScheduleDTO)
    def create_schedule(self, input_data: ScheduleCreateManuallyDTO):
        '''populates the table with provided input
        to be used for creation, not editing data
        if the schedule for this group && semester && day && lesson already exists, returns error

        requires manual input of all data, does not support auto generation for fields
        supports enum classes as input options for semester, weekday, lesson and class type
        as a result populates those fields with data matching with primary tables in db

        returns the last inserted info'''

        already_exists = schedule_service.check_schedule(db=db, semester=input_data.semester, group=input_data.group, weekday=input_data.weekday, lesson_number=input_data.lesson_number);
        if already_exists:
            raise HTTPException(status_code=400, detail=f'''Schedule already exists! (Group: {input_data.group}; Weekday: {input_data.weekday}; Lesson: {input_data.lesson_number}; Semester: {input_data.semester}. If you want to change schedule - use change form, please!''');
        return schedule_service.fill_schedule_manually(self, input_data);

    #admins only
    @router.post(ApiSpec.SCHEDULE_AUTO, status_code=201)
    def create_schedule_auto(self,
                             semester: int,
                             weekday: WeekdaysEnum,
                             lesson_number: int,
                             group_number: int,
                             module_id: int,
                             class_type: ClassTypesEnum):
        '''checks if the provided group_number is busy for the provided date/time
        if not, checks if there are teachers to be assigned for provided module and class type:
        - either not busy ones related to this module
            then first empty romm is assigned as a room
        - or those who have the same module and class tipe lesson at provided date/time
            assignes such teacher and room, sets teacher and room busy
        sets group busy and commit new row to schedule database
        if group is busy, or there are no options with teachers, rises HTTPException'''

        group_busy_flag = group_service.check_group_busy(db=self.db, group_number=group_number, weekday=weekday, lesson_number=lesson_number);

        if group_busy_flag == True:
            raise HTTPException(status_code=400, detail=f'''Group {group_number} in already busy on that time! Choose other conditions or use update!''');

        attempt = schedule_service.autofill_schedule(db=self.db,
                                      semester=semester,
                                      weekday=weekday,
                                      lesson_number=lesson_number,
                                      group_number=group_number,
                                      module_id=module_id,
                                      class_type=class_type);
        if attempt == False:
            raise HTTPException(status_code=400, detail=f'''All teachers are busy for provided module-type pair! Please choose other conditions!''');
        else:
            return attempt;

    #----------------------------
    # READ endpoints
    #----------------------------

    #students and teachers
    @router.get(ApiSpec.SCHEDULE_GROUP, response_model=List[ScheduleGroupResponseDTO])
    def read_schedule_by_group(self, semester: SemestersEnum, group: int, skip: int = 0, limit: int = 100):

        '''takes semester number and group number as an input
        returns all rows from 'schedule' table for provided group and semester'''

        schedule = schedule_service.get_schedule_by_group(db=self.db, semester=semester, group=group);
        return schedule;

    #students and teachers
    @router.get(ApiSpec.SCHEDULE_TEACHER, response_model=List[ScheduleTeacherResponseDTO])
    def read_schedule_by_teacher(self, semester: SemestersEnum, teacher_id: int, skip: int = 0, limit: int = 100):

        '''takes semester number and teacher's id as an input
        returns all rows from 'schedule' table for provided teacher and semester'''

        schedule = schedule_service.get_schedule_by_teacher_id(db=self.db, semester=semester, teacher_id=teacher_id);
        return schedule;

    #----------------------------
    # UPDATE endpoints
    #----------------------------

    #admins and teachers
    @router.patch(ApiSpec.SCHEDULE)
    def patch_schedule_row(self,
                          semester: SemestersEnum,
                          group: int,
                          weekday: WeekdaysEnum,
                          lesson_number: LessonsEnum,
                          module: str = None,
                          class_type: ClassTypesEnum = None,
                          room: int = None,
                          teacher: str = None):

        update = schedule_service.update_schedule(db=self.db, semester=semester, group=group, weekday=weekday,
                             lesson_number=lesson_number, module=module,
                             class_type=class_type, room=room, teacher=teacher);

        return update;

    #----------------------------
    # DELETE endpoints
    #----------------------------

    #admins only
    @router.delete(ApiSpec.SCHEDULE, responses={200: {'model': str}})
    def delete_schedule(self, semester: SemestersEnum, group: int = None):

        '''deletes the rows from the table
        requires semester argument, additional argument - group, by default set to null

        if only semester argument is provided - deletes schedule for the named semester for all groups
        if group number is provided as well - deletes only group schedule for the provided semester

        does not affect table existance'''

        schedule_service.clear_table(db=self.db, semester=semester, group=group);
        if group == None:
            return JSONResponse(status_code=200, content={'message': f'Schedule for {semester} semester was successfully deleted for all groups!'})
        else:
            return JSONResponse(status_code=200, content={'message': f'Schedule for group {group} for {semester} semester was successfully deleted!'})