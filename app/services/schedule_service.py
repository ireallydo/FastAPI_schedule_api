from sorcery import dict_of

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func;
from sqlalchemy.orm import Session, joinedload, defaultload, join, contains_eager, PropComparator;

from db.models import *
from db.dto import *
from db.dao import schedule_dao
from db.enums import WeekdaysEnum, LessonsEnum, ClassTypesEnum, SemestersEnum

from services import teacher_service, module_service, room_service, group_service


def fill_schedule_manually(db, input_data: ScheduleCreateManuallyDTO):
    '''function for fully manual creation of schedule, has no specific checks or constraints'''

    # input_data.weekday = translate_enum_weekday(db, input_data.weekday);
    # input_data.class_type = translate_enum_class_type(db, input_data.class_type);

    new_line = schedule_dao.fill_manually(db, input_data)

    return new_line

def autofill_schedule(db: Session, input_data: ScheduleCreateDTO):

    module = module_service.get_by_name_and_type(db, input_data.module_name, input_data.class_type)
    module_id = module.id
    teachers_list = teacher_service.get_teachers_by_module(db, module_id)

    for teacher in teachers_list:
        teacher_busy = teacher_service.check_teacher_busy(db, teacher, input_data.weekday, input_data.lesson_number)
        if teacher_busy:
            teacher_busy_flag = teacher_busy.is_busy
        else:
            teacher_busy_flag = False

        if teacher_busy_flag == False:
            teacher_id = teacher
            teacher_service.set_teacher_busy(db, teacher_id, input_data.weekday, input_data.lesson_number)
            room_number = None
            break

        if teacher_busy_flag == True and teacher == teachers_list[-1]:
            join_groups_check = query_db_for_same_class(db, teachers_list, module_id, input_data)
            if join_groups_check == False:
                return False
            else:
                (teacher_id, room_number) = join_groups_check
        else:
            continue

    if not room_number:
        try:
            appropriate_rooms = room_service.get_rooms_by_class_type(db, input_data.class_type)
            for room in appropriate_rooms:
                print(room.id)
                room_in_busy_table = room_service.check_room_busy(db, room.id, input_data.weekday, input_data.lesson_number)
                if room_in_busy_table:
                    if room_in_busy_table.is_busy == False:
                        room_number = room_in_busy_table.room_number
                    else:
                        continue
                else:
                    room_number = room.room_number
                    break
        except:
            raise HTTPException(status_code=400, detail=f'''Все доступные кабинеты для указанного вида занятий в указанное время заняты.''')

    new_line_dict = dict_of(input_data.semester, input_data.group_number,input_data.weekday, input_data.lesson_number, module_id, input_data.class_type, room_number, teacher_id)
    new_line = ScheduleModel(**new_line_dict)
    db.add(new_line);
    db.commit();
    db.refresh(new_line);

    return new_line



def query_db_for_same_class(db: Session, teachers_list: list, module_id, input_data):
    '''checks if there are classes in the schedule with the same teacher, module, class_type at the same time
    for teachers in the teachers_list
    if there are - returns a tuple of teacher_id and room_number of such classes
    is used in autofill_schedule function'''

    for teacher in teachers_list:
        can_join_lessons = schedule_dao.join_lessons_check(db, teacher, module_id, input_data)
        if can_join_lessons:
            chosen_teacher_id = teacher
            chosen_room_number = can_join_lessons.room
            return chosen_teacher_id, chosen_room_number
    return False





# -----------------------------------------------------------------
# read functions
# -----------------------------------------------------------------

def check_schedule(db, input_data: ScheduleCreateManuallyDTO):

    # db_weekday = translate_enum_weekday(input_data.weekday);

    return schedule_dao.check_exists(db, input_data)


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
