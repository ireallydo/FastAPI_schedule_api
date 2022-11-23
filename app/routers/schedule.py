from typing import List
from sorcery import dict_of

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from services import schedule_service, group_service, module_service

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


@cbv(router)
class ScheduleView:
    # dependencies as class attributes
    db: Session = Depends(get_db)


    #admins only
    @router.post(ApiSpec.SCHEDULE_AUTO, status_code=200, response_model=ScheduleOutDTO)
    def create_schedule_auto(self, input_data: ScheduleCreateDTO):
        '''checks if the provided group_number is busy for the provided date/time
        if not, checks if there are teachers to be assigned for provided module and class type:
        - either not busy ones related to this module
            then first empty romm is assigned as a room
        - or those who have the same module and class tipe lesson at provided date/time
            assignes such teacher and room, sets teacher and room busy
        sets group busy and commit new row to schedule database
        if group is busy, or there are no options with teachers, rises HTTPException'''

        # check if the group is busy at the provided date and time
        group_busy_dict: GroupBusyDTO = dict_of(input_data.weekday, input_data.lesson_number, input_data.group_number)
        group_in_busy_tbl = group_service.check_group_busy(self.db, group_busy_dict)
        if group_in_busy_tbl:
            group_busy_flag=group_in_busy_tbl.is_busy
            if group_busy_flag == True:
                raise HTTPException(status_code=400, detail=f'''Группа уже занята!''')

        # get module id from module name
        module = module_service.get_by_name_and_type(self.db, input_data.module_name, input_data.class_type)
        module_id = module.id

        # try to find a teacher and a room for provided info
        (teacher_id, room_number) = schedule_service.find_teacher(self.db, input_data, module_id)
        print(teacher_id, room_number)

        # check if the room is found, if not - find a spare room
        room_number = schedule_service.find_room(self.db, input_data, room_number)
        print(room_number)

        # post new row in the schedule table
        schedule_row = schedule_service.post_schedule(self.db, input_data, module_id, room_number, teacher_id)

        # set group busy
        group_busy_input = dict_of(input_data.group_number, input_data.weekday, input_data.lesson_number)
        if group_in_busy_tbl:
                group_service.set_group_busy(self.db, group_busy_input)
        else:
            group_service.create_group_busy(self.db, group_busy_input)

        # decode schedule_row into human-readable output
        schedule_output = schedule_service.make_schedule_output(self.db, schedule_row, input_data)

        return schedule_output


    #admins only
    @router.post(ApiSpec.SCHEDULE_MANUAL, status_code=201, response_model=ScheduleOutDTO)
    def create_schedule(self, input_data: ScheduleCreateManuallyDTO):
        '''populates the table with provided input
        to be used for creation
        if the schedule for this group && semester && day && lesson already exists, returns error
        requires manual input of all data, does not support auto generation for fields'''

        already_exists = schedule_service.check_schedule(self.db, input_data)
        print('CHECKED!!')
         # semester=input_data.semester, group=input_data.group, weekday=input_data.weekday, lesson_number=input_data.lesson_number)
        if already_exists:
            raise HTTPException(status_code=400, detail=f'''Schedule already exists! (Group: {input_data.group}; Weekday: {input_data.weekday}; Lesson: {input_data.lesson_number}; Semester: {input_data.semester}. If you want to change schedule - use change form, please!''');
        return schedule_service.fill_schedule_manually(self.db, input_data);


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
