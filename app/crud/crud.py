from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from models import *
from schemas import *
from enums import *

from db import engine, Base;


enum_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5};

# -----------------------------------------------------------------
# auth functions
# -----------------------------------------------------------------

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first();

def get_user_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first();

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all();

# -----------------------------------------------------------------
# create functions
# -----------------------------------------------------------------

def fill_schedule_manually(db: Session, input_data: ScheduleCreateManually):
    '''function for fully manual creation of schedule, has no specific checks or constraints'''

    input_data.weekday = translate_enum_weekday(db, input_data.weekday);
    input_data.class_type = translate_enum_class_type(db, input_data.class_type);

    new_line = models.Schedule(**input_data.dict());

    db.add(new_line);
    db.commit();
    db.refresh(new_line);

    return new_line;

def autofill_schedule(db: Session, semester: int, weekday: enum_models.Weekdays, lesson_number: int, group_number: int, module_id: int, class_type: enum_models.ClassTypes):

    db_weekday = translate_enum_weekday(db, weekday);
    group_id = get_group_id_by_number(db, group_number);
    db_class_type = translate_enum_class_type(db, class_type);
    chosen_room_number = 0;

    teachers_list = teachers_id_by_module(db, module_id=module_id);

    for teacher in teachers_list:
        teacher_busy_flag = check_teacher_busy(db=db, teacher_id=teacher, weekday=db_weekday, lesson=lesson_number);

        if teacher_busy_flag == False:
            chosen_teacher_id = teacher;
            set_teacher_busy(db=db, teacher_id=chosen_teacher_id, weekday=db_weekday, lesson=lesson_number);
            break;

        if teacher_busy_flag == True and teacher == teachers_list[-1]:
            join_groups_check = query_db_for_same_class(db=db,
                                                        teachers_list=teachers_list,
                                                        semester=semester,
                                                        weekday=db_weekday,
                                                        lesson_number=lesson_number,
                                                        module_id=module_id,
                                                        class_type=db_class_type);

            if join_groups_check == False:
                return False;
            else:
                chosen_teacher_id = join_groups_check[0];
                chosen_room_number = join_groups_check[1];
        else:
            continue;

    if chosen_room_number == 0:
        room_id = check_room_busy(db=db, weekday=db_weekday, lesson=lesson_number);
        chosen_room_number = get_room_number_by_id(db=db, room_id=room_id);

    set_group_busy(db=db, group_id=group_id, weekday=db_weekday, lesson=lesson_number);

    new_line = models.Schedule(semester=semester,
                               group=group_number,
                               weekday=db_weekday,
                               lesson_number=lesson_number,
                               module_id=module_id,
                               class_type=db_class_type,
                               room=chosen_room_number,
                               teacher_id=chosen_teacher_id);

    db.add(new_line);
    db.commit();
    db.refresh(new_line);

    return new_line;

# -----------------------------------------------------------------
# read functions
# -----------------------------------------------------------------

def check_schedule(db: Session,
                  semester: enum_models.Semesters,
                  group: int,
                  weekday: enum_models.Weekdays,
                  lesson_number: enum_models.Lessons):

    db_weekday = translate_enum_weekday(db, weekday);

    return db.query(models.Schedule).filter(models.Schedule.group==group,
                                            models.Schedule.semester==semester,
                                            models.Schedule.weekday==db_weekday,
                                            models.Schedule.lesson_number==lesson_number).all();


def get_schedule_by_group(db: Session, semester: enum_models.Semesters, group: int, skip: int = 0, limit: int = 100):

    schedule = db.query(models.Weekday).join(models.Weekday.lessons).\
                                    join(models.Lesson.schedule.and_(models.Schedule.weekday==models.Weekday.name,
                                                                     models.Schedule.group==group,
                                                                     models.Schedule.semester==semester)).\
                                    join(models.Schedule.modules).options(contains_eager(models.Weekday.lessons).\
                                                                          contains_eager(models.Lesson.schedule).\
                                                                          contains_eager(models.Schedule.modules)).order_by(models.Lesson.id).offset(skip).limit(limit).all();

    return schedule;


def get_schedule_by_teacher_id(db: Session, semester: enum_models.Semesters, teacher_id: int, skip: int = 0, limit: int = 100):

    schedule = db.query(models.Weekday).join(models.Weekday.lessons).\
                                    join(models.Lesson.schedule.and_(models.Schedule.weekday==models.Weekday.name,
                                                                    models.Schedule.teacher_id==teacher_id,
                                                                    models.Schedule.semester==semester)).\
                                    join(models.Schedule.modules).options(contains_eager(models.Weekday.lessons).\
                                                                          contains_eager(models.Lesson.schedule).\
                                                                          contains_eager(models.Schedule.modules)).order_by(models.Lesson.id).offset(skip).limit(limit).all();

    return schedule;

# -----------------------------------------------------------------
# update functions
# -----------------------------------------------------------------

def update_schedule(db: Session,
                    semester: enum_models.Semesters,
                    group: int,
                    weekday: enum_models.Weekdays,
                    lesson_number: enum_models.Lessons,
                    module: str = None,
                    class_type: enum_models.ClassTypes = None,
                    room: int = None,
                    teacher: str = None):

    if class_type == None:
        db_class_type = models.Schedule.class_type;
    else:
        db_class_type = translate_enum_class_type(db, class_type);

    if room == None:
        room = models.Schedule.room;

    if module == None:
        module = models.Schedule.module;

    if teacher == None:
        teacher = models.Schedule.teacher;

    db_weekday = translate_enum_weekday(db, weekday);

    db.query(models.Schedule).filter(models.Schedule.semester==semester,
                                     models.Schedule.group==group,
                                     models.Schedule.lesson_number==lesson_number,
                                     models.Schedule.weekday==db_weekday).update([(models.Schedule.room, room),
                                                                                  (models.Schedule.module, module),
                                                                                  (models.Schedule.class_type, db_class_type),
                                                                                  (models.Schedule.teacher, teacher)
                                                                                  ],
                                                                                 update_args={'preserve_parameter_order':True});
    db.commit();

# -----------------------------------------------------------------
# delete functions
# -----------------------------------------------------------------
def clear_table(db: Session, semester: enum_models.Semesters, group: int = None):
    if group == None:
        db.query(models.Schedule).filter(models.Schedule.semester==semester).delete();
        db.commit();
    else:
        db.query(models.Schedule).filter(models.Schedule.semester==semester, models.Schedule.group==group).delete();
        db.commit();

# -----------------------------------------------------------------
# enum translation functions
# -----------------------------------------------------------------

def translate_enum_weekday(db: Session, weekday: enum_models.Weekdays):
    '''is used to support mutilingual databases while using latin for input
    takes a value from the enum model as an input
    returns the matching weekday value from the 'weekdays' table in db
    e.g. "Monday" will return a proper weekday name from database in accordance with the enum attribute value'''
    if str(enum_models.Weekdays(weekday).name) in enum_dict.keys():
        day_id=enum_dict[str(enum_models.Weekdays(weekday).name)];
        db_weekday = db.query(models.Weekday.name).where(models.Weekday.id==day_id).all();
    return db_weekday[0][0];

def translate_enum_class_type(db: Session, class_type: enum_models.ClassTypes):
    '''is used to support mutilingual databases while using latin for input
    takes a class_type value from the enum model as an input
    returns the matching type of class value from the 'class_types' table in db
    e.g. "lecture" will return a proper class_type name from database in accordance with the enum attribute value'''
    if str(enum_models.ClassTypes(class_type).name) in enum_dict.keys():
        class_type_id=enum_dict[str(enum_models.ClassTypes(class_type).name)];
        db_class_type = db.query(models.TypeOfClass.name).where(models.TypeOfClass.id==class_type_id).all();
    return db_class_type[0][0];

# -----------------------------------------------------------------
# tech read functions
# -----------------------------------------------------------------

def get_group_id_by_number(db: Session, group: int):
    '''takes a group number as input, returns group id as an int'''
    request_group_id = db.query(models.AcademicGroup.id).where(models.AcademicGroup.number==group);
    group_id = request_group_id[0][0];
    return group_id;

def get_room_number_by_id(db:Session, room_id: int):
    '''takes a room id and returns correspondig room number'''
    request_room_number = db.query(models.Room.number).where(models.Room.id==room_id);
    room_number = request_room_number[0][0];
    return room_number;

def teachers_id_by_module(db: Session, module_id: int):
    '''takes module id as an input, outputs the list of corresponding teachers ids'''
    teachers_id_by_module = db.query(models.teachers_modules).where(models.teachers_modules.c.Module_id==module_id).all();

    teachers_list = [];

    for instance in teachers_id_by_module:
        teachers_list.append(instance['Teacher_id']);

    return teachers_list;

def query_db_for_same_class(db: Session, teachers_list: list, semester: int, weekday: str, lesson_number: int, module_id: int, class_type: str):
    '''checks if there are classes in the schedule with the same teacher, module, class_type at the same time
    for teachers in the teachers_list
    if there are - returns a tuple of teacher_id and room_number of such classes
    is used in autofill_schedule function'''

    for teacher in teachers_list:

        can_join_lessons = db.query(models.Schedule).filter(models.Schedule.teacher_id==teacher,
                                    models.Schedule.semester==semester,
                                    models.Schedule.weekday==weekday,
                                    models.Schedule.lesson_number==lesson_number,
                                    models.Schedule.module_id==module_id,
                                    models.Schedule.class_type==class_type).all();
        if can_join_lessons:
            query_dict = can_join_lessons[0];
            chosen_teacher_id = teacher;
            chosen_room_number = query_dict.room;
            return chosen_teacher_id, chosen_room_number;

    return False;

def check_group_busy(db: Session, group_number: int, weekday: enum_models.Weekdays, lesson_number: int):
    '''takes group id, weekday (str) and lesson number as input
    returns false flag if the group is NOT busy and true flag is the group IS busy'''

    db_weekday = translate_enum_weekday(db, weekday);
    group_id = get_group_id_by_number(db, group_number);

    db_request = db.query(models.GroupBusy.is_busy).where(models.GroupBusy.group_id==group_id,
                                                           models.GroupBusy.weekday==db_weekday,
                                                           models.GroupBusy.lesson==lesson_number).all();

    db_dict = db_request[0];

    if db_dict['is_busy']== False:
        return False;
    else:
        return True;

def check_teacher_busy(db: Session, teacher_id: int, weekday: str, lesson: int):
    '''takes teacher id, weekday (str) and lesson number as input
    returns false flag if the teacher is NOT busy and true flag is the teacher IS busy'''

    db_request = db.query(models.TeacherBusy.is_busy).where(models.TeacherBusy.teacher_id==teacher_id,
                                                           models.TeacherBusy.weekday==weekday,
                                                           models.TeacherBusy.lesson==lesson).all();

    db_dict = db_request[0];

    if db_dict['is_busy']== False:
        return False;
    else:
        return True;

def check_room_busy(db: Session, weekday: str, lesson: int):
    '''takes weekday and lesson as input
    returns one room with is_busy flag set to false (empty room)'''

    db_request = db.query(models.RoomBusy).where(models.RoomBusy.weekday==weekday,
                                                 models.RoomBusy.lesson==lesson,
                                                 models.RoomBusy.is_busy==False).first();

    return db_request.room_id;

# -----------------------------------------------------------------
# tech create functions
# -----------------------------------------------------------------

def set_group_busy(db:Session, group_id: int, weekday: str, lesson: int):
    '''takes group id, weekday (str) and lesson number as input
    sets the is_busy flag to true'''

    db.query(models.GroupBusy).filter(models.GroupBusy.group_id==group_id,
                                             models.GroupBusy.weekday==weekday,
                                             models.GroupBusy.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
    db.commit();

def set_teacher_busy(db:Session, teacher_id: int, weekday: str, lesson: int):
    '''takes teacher id, weekday (str) and lesson number as input
    sets the is_busy flag to true'''

    db.query(models.TeacherBusy).filter(models.TeacherBusy.teacher_id==teacher_id,
                                             models.TeacherBusy.weekday==weekday,
                                             models.TeacherBusy.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
    db.commit();

#-----------------------------that's all, folks---------------------------------
