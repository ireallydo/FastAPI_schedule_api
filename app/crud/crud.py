from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import *
from schemas import *
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum


enum_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5};

# -----------------------------------------------------------------
# auth functions
# -----------------------------------------------------------------

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first();

def get_user_by_email(db: Session, email:str):
    return db.query(UserModel).filter(UserModel.email == email).first();

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all();

# -----------------------------------------------------------------
# create functions
# -----------------------------------------------------------------

def fill_schedule_manually(db: Session, input_data: ScheduleCreateManually):
    '''function for fully manual creation of schedule, has no specific checks or constraints'''

    input_data.weekday = translate_enum_weekday(db, input_data.weekday);
    input_data.class_type = translate_enum_class_type(db, input_data.class_type);

    new_line = ScheduleModel(**input_data.dict());

    db.add(new_line);
    db.commit();
    db.refresh(new_line);

    return new_line;

def autofill_schedule(db: Session, semester: int, weekday: WeekdaysEnum, lesson_number: int, group_number: int, module_id: int, class_type: ClassTypesEnum):

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

    new_line = ScheduleModel(semester=semester,
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
                  semester: SemestersEnum,
                  group: int,
                  weekday: WeekdaysEnum,
                  lesson_number: LessonsEnum):

    db_weekday = translate_enum_weekday(db, weekday);

    return db.query(ScheduleModel).filter(ScheduleModel.group==group,
                                            ScheduleModel.semester==semester,
                                            ScheduleModel.weekday==db_weekday,
                                            ScheduleModel.lesson_number==lesson_number).all();


def get_schedule_by_group(db: Session, semester: SemestersEnum, group: int, skip: int = 0, limit: int = 100):

    schedule = db.query(WeekdayModel).join(WeekdayModel.lessons).\
                                    join(LessonModel.schedule.and_(ScheduleModel.weekday==WeekdayModel.name,
                                                                     ScheduleModel.group==group,
                                                                     ScheduleModel.semester==semester)).\
                                    join(ScheduleModel.modules).options(contains_eager(WeekdayModel.lessons).\
                                                                          contains_eager(LessonModel.schedule).\
                                                                          contains_eager(ScheduleModel.modules)).order_by(LessonModel.id).offset(skip).limit(limit).all();

    return schedule;


def get_schedule_by_teacher_id(db: Session, semester: SemestersEnum, teacher_id: int, skip: int = 0, limit: int = 100):

    schedule = db.query(WeekdayModel).join(WeekdayModel.lessons).\
                                    join(LessonModel.schedule.and_(ScheduleModel.weekday==WeekdayModel.name,
                                                                    ScheduleModel.teacher_id==teacher_id,
                                                                    ScheduleModel.semester==semester)).\
                                    join(ScheduleModel.modules).options(contains_eager(WeekdayModel.lessons).\
                                                                          contains_eager(LessonModel.schedule).\
                                                                          contains_eager(ScheduleModel.modules)).order_by(LessonModel.id).offset(skip).limit(limit).all();

    return schedule;

# -----------------------------------------------------------------
# update functions
# -----------------------------------------------------------------

def update_schedule(db: Session,
                    semester: SemestersEnum,
                    group: int,
                    weekday: WeekdaysEnum,
                    lesson_number: LessonsEnum,
                    module: str = None,
                    class_type: ClassTypesEnum = None,
                    room: int = None,
                    teacher: str = None):

    if class_type == None:
        db_class_type = ScheduleModel.class_type;
    else:
        db_class_type = translate_enum_class_type(db, class_type);

    if room == None:
        room = ScheduleModel.room;

    if module == None:
        module = ScheduleModel.module;

    if teacher == None:
        teacher = ScheduleModel.teacher;

    db_weekday = translate_enum_weekday(db, weekday);

    db.query(ScheduleModel).filter(ScheduleModel.semester==semester,
                                     ScheduleModel.group==group,
                                     ScheduleModel.lesson_number==lesson_number,
                                     ScheduleModel.weekday==db_weekday).update([(ScheduleModel.room, room),
                                                                                  (ScheduleModel.module, module),
                                                                                  (ScheduleModel.class_type, db_class_type),
                                                                                  (ScheduleModel.teacher, teacher)
                                                                                  ],
                                                                                 update_args={'preserve_parameter_order':True});
    db.commit();

# -----------------------------------------------------------------
# delete functions
# -----------------------------------------------------------------
def clear_table(db: Session, semester: SemestersEnum, group: int = None):
    if group == None:
        db.query(ScheduleModel).filter(ScheduleModel.semester==semester).delete();
        db.commit();
    else:
        db.query(ScheduleModel).filter(ScheduleModel.semester==semester, ScheduleModel.group==group).delete();
        db.commit();

# -----------------------------------------------------------------
# enum translation functions
# -----------------------------------------------------------------

def translate_enum_weekday(db: Session, weekday: WeekdaysEnum):
    '''is used to support mutilingual databases while using latin for input
    takes a value from the enum model as an input
    returns the matching weekday value from the 'weekdays' table in db
    e.g. "Monday" will return a proper weekday name from database in accordance with the enum attribute value'''
    if str(WeekdaysEnum(weekday).name) in enum_dict.keys():
        day_id=enum_dict[str(WeekdaysEnum(weekday).name)];
        db_weekday = db.query(WeekdayModel.name).where(WeekdayModel.id==day_id).all();
    return db_weekday[0][0];

def translate_enum_class_type(db: Session, class_type: ClassTypesEnum):
    '''is used to support mutilingual databases while using latin for input
    takes a class_type value from the enum model as an input
    returns the matching type of class value from the 'class_types' table in db
    e.g. "lecture" will return a proper class_type name from database in accordance with the enum attribute value'''
    if str(ClassTypesEnum(class_type).name) in enum_dict.keys():
        class_type_id=enum_dict[str(ClassTypesEnum(class_type).name)];
        db_class_type = db.query(TypeOfClassModel.name).where(TypeOfClassModel.id==class_type_id).all();
    return db_class_type[0][0];

# -----------------------------------------------------------------
# tech read functions
# -----------------------------------------------------------------

def get_group_id_by_number(db: Session, group: int):
    '''takes a group number as input, returns group id as an int'''
    request_group_id = db.query(AcademicGroupModel.id).where(AcademicGroupModel.number==group);
    group_id = request_group_id[0][0];
    return group_id;

def get_room_number_by_id(db:Session, room_id: int):
    '''takes a room id and returns correspondig room number'''
    request_room_number = db.query(RoomModel.number).where(RoomModel.id==room_id);
    room_number = request_room_number[0][0];
    return room_number;

def teachers_id_by_module(db: Session, module_id: int):
    '''takes module id as an input, outputs the list of corresponding teachers ids'''
    teachers_id_by_module = db.query(teachers_to_modules).where(teachers_to_modules.c.Module_id==module_id).all();

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

        can_join_lessons = db.query(ScheduleModel).filter(ScheduleModel.teacher_id==teacher,
                                    ScheduleModel.semester==semester,
                                    ScheduleModel.weekday==weekday,
                                    ScheduleModel.lesson_number==lesson_number,
                                    ScheduleModel.module_id==module_id,
                                    ScheduleModel.class_type==class_type).all();
        if can_join_lessons:
            query_dict = can_join_lessons[0];
            chosen_teacher_id = teacher;
            chosen_room_number = query_dict.room;
            return chosen_teacher_id, chosen_room_number;

    return False;

def check_group_busy(db: Session, group_number: int, weekday: WeekdaysEnum, lesson_number: int):
    '''takes group id, weekday (str) and lesson number as input
    returns false flag if the group is NOT busy and true flag is the group IS busy'''

    db_weekday = translate_enum_weekday(db, weekday);
    group_id = get_group_id_by_number(db, group_number);

    db_request = db.query(GroupBusyModel.is_busy).where(GroupBusyModel.group_id==group_id,
                                                           GroupBusyModel.weekday==db_weekday,
                                                           GroupBusyModel.lesson==lesson_number).all();

    db_dict = db_request[0];

    if db_dict['is_busy']== False:
        return False;
    else:
        return True;

def check_teacher_busy(db: Session, teacher_id: int, weekday: str, lesson: int):
    '''takes teacher id, weekday (str) and lesson number as input
    returns false flag if the teacher is NOT busy and true flag is the teacher IS busy'''

    db_request = db.query(TeacherBusyModel.is_busy).where(TeacherBusyModel.teacher_id==teacher_id,
                                                           TeacherBusyModel.weekday==weekday,
                                                           TeacherBusyModel.lesson==lesson).all();

    db_dict = db_request[0];

    if db_dict['is_busy']== False:
        return False;
    else:
        return True;

def check_room_busy(db: Session, weekday: str, lesson: int):
    '''takes weekday and lesson as input
    returns one room with is_busy flag set to false (empty room)'''

    db_request = db.query(RoomBusyModel).where(RoomBusyModel.weekday==weekday,
                                                 RoomBusyModel.lesson==lesson,
                                                 RoomBusyModel.is_busy==False).first();

    return db_request.room_id;

# -----------------------------------------------------------------
# tech create functions
# -----------------------------------------------------------------

def set_group_busy(db:Session, group_id: int, weekday: str, lesson: int):
    '''takes group id, weekday (str) and lesson number as input
    sets the is_busy flag to true'''

    db.query(GroupBusyModel).filter(GroupBusyModel.group_id==group_id,
                                             GroupBusyModel.weekday==weekday,
                                             GroupBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
    db.commit();

def set_teacher_busy(db:Session, teacher_id: int, weekday: str, lesson: int):
    '''takes teacher id, weekday (str) and lesson number as input
    sets the is_busy flag to true'''

    db.query(TeacherBusyModel).filter(TeacherBusyModel.teacher_id==teacher_id,
                                             TeacherBusyModel.weekday==weekday,
                                             TeacherBusyModel.lesson==lesson).update({'is_busy': True}, synchronize_session="fetch");
    db.commit();

#-----------------------------that's all, folks---------------------------------
