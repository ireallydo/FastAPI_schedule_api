from http import HTTPStatus
from typing import Any, NoReturn
from fastapi import HTTPException
from db.models import ScheduleModel
from db.dto import ScheduleCreateDTO, BusyDTO, ScheduleCreateManuallyDTO,\
    ScheduleOutDTO, TeacherInScheduleDTO,\
    ClassesGroupDTO, WeekdaysGroupDTO, GroupScheduleDTO,\
    ClassesTeacherDTO, WeekdaysTeacherDTO, TeacherScheduleDTO
from db.dao import schedule_dao, ScheduleDAO
from db.enums import SemestersEnum
from services.group_service import group_service, GroupService
from services.teacher_service import teacher_service, TeacherService
from services.module_service import module_service, ModuleService
from services.lesson_service import lesson_service, LessonService
from services.room_service import room_service, RoomService
from loguru import logger


class ScheduleService:

    def __init__(self, schedule_dao: ScheduleDAO, group_service: GroupService, room_service: RoomService,
                 teacher_service: TeacherService, lesson_service: LessonService, module_service: ModuleService):
        self._schedule_dao = schedule_dao
        self._group_service = group_service
        self._room_service = room_service
        self._teacher_service = teacher_service
        self._lesson_service = lesson_service
        self._module_service = module_service

    async def create_auto(self, item: ScheduleCreateDTO) -> ScheduleOutDTO:
        logger.info("ScheduleService: Create schedule automatically")
        logger.trace(f"ScheduleService: Create schedule automatically with passed data: {item}")
        # check if provided lesson is in db and group is not busy
        await self.check_for_schedule(item)
        # get module class type
        module = await self._module_service.get_by_id(item.module_id)
        if module is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail=f"There is no module with provided id: {item.module_id}")
        class_type = module.class_type
        # check if there are free rooms to hold a new lesson of provided class type at this time
        free_room = await self._room_service.get_free_room(class_type, item.weekday, item.lesson_number, item.semester)
        if free_room is not None:
            # get list of all teachers who can teach the provided module
            all_teachers = module.teachers
            # find the first teacher in the list  who's not busy at provided time
            for teacher in all_teachers:
                teacher_busy = await self._teacher_service.check_teacher_busy(teacher.id,
                                                                              item.weekday,
                                                                              item.lesson_number)
                if teacher_busy is None or not teacher_busy.is_busy:
                    busy = BusyDTO(
                        is_busy=True,
                        weekday=item.weekday,
                        lesson=item.lesson_number,
                        semester=item.semester
                    )
                    await self._teacher_service.set_teacher_busy(teacher.id, busy)
                    await self._group_service.set_group_busy(item.group_number, busy)
                    await self._room_service.set_room_busy(free_room.room_number, busy)
                    schedule_obj = ScheduleCreateManuallyDTO(
                        semester=item.semester,
                        weekday=item.weekday,
                        lesson_number=item.lesson_number,
                        group_number=item.group_number,
                        module_id=item.module_id,
                        room_number=free_room.room_number,
                        teacher_id=teacher.id
                    )
                    schedule = await self._schedule_dao.create(schedule_obj)
                    return await self.__make_out_obj(schedule)
        # if didn't find any free teacher, or room,
        # find if there's the same module at this time in the schedule
        same_schedule = await self._schedule_dao.get_by(
            semester=item.semester,
            weekday=item.weekday,
            lesson_number=item.lesson_number,
            module_id=item.module_id
        )
        if same_schedule is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='There are no available options of teachers and/or rooms for this class.')
        else:
            busy = BusyDTO(
                is_busy=True,
                weekday=item.weekday,
                lesson=item.lesson_number,
                semester=item.semester
            )
            await self._group_service.set_group_busy(item.group_number, busy)
            # assign the group to the existing teacher and room
            schedule_obj = ScheduleCreateManuallyDTO(
                semester=item.semester,
                weekday=item.weekday,
                lesson_number=item.lesson_number,
                group_number=item.group_number,
                module_id=item.module_id,
                room_number=same_schedule.room_number,
                teacher_id=same_schedule.teacher_id
            )
            schedule = await self._schedule_dao.create(schedule_obj)
            return await self.__make_out_obj(schedule)

    async def create_manually(self, item: ScheduleCreateManuallyDTO) -> ScheduleOutDTO:
        logger.info("ScheduleService: Create schedule manually")
        logger.trace(f"ScheduleService: Create schedule manually with passed data: {item}")
        # check if provided lesson is in db and group is not busy
        await self.check_for_schedule(item)
        # check if room suits the module class type
        room = await self._room_service.get_by_number(item.room_number)
        module = await self._module_service.get_by_id(item.module_id)
        if room.class_type != module.class_type:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Room class type does not match module class type.')
        # check if room is busy
        room_busy = await self._room_service.check_room_busy(room.id, item.weekday, item.lesson, item.semester)
        if room_busy is not None and room_busy.is_busy:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Room is already busy at provided time.')
        # check if teacher can be assigned to the module
        teacher_modules = await self._teacher_service.get_modules(teacher_id)
        if teacher_modules:
            module_ids = [str(mod.id) for mod in teacher_modules]
            if item.module_id not in module_ids:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                    detail='Teacher cannot be assigned to the module.')
        else:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Teacher cannot be assigned to the module.')
        # check if teacher is busy
        teacher_busy = await self._teacher_service.check_teacher_busy(teacher_id,
                                                                      item.weekday,
                                                                      item.lesson_number,
                                                                      item.semester)
        if teacher_busy is not None and teacher_busy.is_busy:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Teacher is already busy at provided time.')
        # if all checks are passed - set group, room and teacher busy and create schedule
        # set teacher busy
        busy = BusyDTO(
            is_busy=True,
            weekday=item.weekday,
            lesson=item.lesson_number,
            semester=item.semester
        )
        await self._teacher_service.set_teacher_busy(teacher_id, busy)
        # set group busy
        await self._group_service.set_group_busy(item.group_number, busy)
        # set room busy
        await self._room_service.set_room_busy(item.room_number, busy)
        # use teacher and room to make a schedule
        schedule_obj = ScheduleCreateManuallyDTO(
            semester=item.semester,
            weekday=item.weekday,
            lesson_number=item.lesson_number,
            group_number=item.group_number,
            module_id=item.module_id,
            room_number=item.room_number,
            teacher_id=item.teacher_id
        )
        schedule = await self._schedule_dao.create(schedule_obj)
        return await self.__make_out_obj(schedule)

    async def check_for_schedule(self, item: Any) -> NoReturn:
        logger.info("ScheduleService: Check if provided lesson is in db and group is not busy")
        # check if provided lesson is in db
        await self._lesson_service.get_by_number(item.lesson_number)
        # check if the group is busy at the provided date and time
        group_busy = await self._group_service.check_group_busy(item.group_number,
                                                                item.weekday,
                                                                item.lesson_number,
                                                                item.semester)
        if group_busy is not None and group_busy.is_busy:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='The group is already busy at provided time.')

    async def __make_out_obj(self, schedule: ScheduleModel) -> ScheduleOutDTO:
        response_obj = ScheduleOutDTO(
            id=schedule.id,
            semester=schedule.semester,
            group_number=schedule.group_number,
            weekday=schedule.weekday,
            lesson=schedule.lessons,
            module=schedule.modules,
            room_number=schedule.room_number,
            teacher=schedule.teachers
        )
        return response_obj

    async def get_all_by(self, *args, **kwargs):
        logger.info("ScheduleService: Get all schedule entries by parameters")
        resp = await self._schedule_dao.get_all_by(*args, **kwargs)
        return resp

    async def get_by_group(self, *args, **kwargs) -> GroupScheduleDTO:
        logger.info("ScheduleService: Get schedule by group number")
        logger.trace(f"ScheduleService: Get schedule by parameters: {kwargs}")
        items = await self.get_all_by(*args, **kwargs)
        weekdays = {}
        for i in items:
            data = ClassesGroupDTO(
                schedule_id=i.id,
                lesson=i.lessons,
                module=i.modules,
                room_number=i.room_number,
                teacher=i.teachers
            )
            if i.weekday in weekdays:
                weekdays[i.weekday].append(data)
            else:
                weekdays[i.weekday] = [data]

        schedule = [WeekdaysGroupDTO(weekday=day, classes=unit) for (day, unit) in weekdays.items()]
        response = GroupScheduleDTO(
            semester=kwargs.get('semester'),
            group_number=kwargs.get('group_number'),
            schedule=schedule
        )
        return response

    async def get_by_teacher(self, *args, **kwargs) -> TeacherScheduleDTO:
        logger.info("ScheduleService: Get schedule by teacher id")
        logger.trace(f"ScheduleService: Get schedule by parameters: {kwargs}")
        items = await self.get_all_by(*args, **kwargs)
        weekdays = {}

        for i in items:
            # don't have id, as joined by groups
            data = ClassesTeacherDTO(
                lesson=i.lessons,
                module=i.modules,
                room_number=i.room_number,
                groups=[i.group_number]
            )
            if i.weekday in weekdays:
                for entry in weekdays[i.weekday]:
                    # join groups
                    if entry.lesson.lesson_number == i.lessons.lesson_number and\
                            entry.module.id == i.modules.id and\
                            entry.room_number == i.room_number:
                        entry.groups.append(i.group_number) if i.group_number not in entry.groups else None
                        break
                    elif entry == weekdays[i.weekday][-1]:
                        weekdays[i.weekday].append(data)
            else:
                weekdays[i.weekday] = [data]
        schedule = [WeekdaysTeacherDTO(weekday=day, classes=unit) for (day, unit) in weekdays.items()]
        teacher = await self._teacher_service.get_by_id(kwargs.get('teacher_id'))
        response = TeacherScheduleDTO(
            semester=kwargs.get('semester'),
            teacher=teacher,
            schedule=schedule
        )
        return response

    async def delete_schedule_entry(self, schedule_id: str) -> NoReturn:
        logger.info("ScheduleService: Delete schedule entry in the database")
        logger.trace(f"ScheduleService: Delete schedule entry with id: {schedule_id}")
        await self._schedule_dao.delete(schedule_id)

    async def clear_semester_schedule(self, semester: SemestersEnum) -> NoReturn:
        logger.info("ScheduleService: Delete all schedule entries of the provided semester")
        logger.trace(f"ScheduleService: Delete schedule entries for semester: {semester}")
        await self._schedule_dao.delete_by(semester=semester)


schedule_service = ScheduleService(schedule_dao, group_service, room_service,
                                   teacher_service, lesson_service, module_service)
