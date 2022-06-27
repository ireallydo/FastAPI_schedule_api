from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
#from sqlalchemy.dialects.mysql import MEDIUMINT, TINYINT, VARCHAR, YEAR

from database import Base

# -----------------------------------------------------------------
# auth class
# -----------------------------------------------------------------
class User(Base):
    ''' '''
    __tablename__ = 'users';

    id = Column(Integer, primary_key=True, index=True);
    username = Column(String(255), unique=True, index=True);
    email = Column(String(255), unique=True, index=True);
    hashed_password = Column(String(255));
    is_active = Column(Boolean, default=True);
    student_id = Column(Integer, ForeignKey('students.id'), unique=True, index=True);
    admin_id = Column(Integer, ForeignKey('admins.id'), unique=True, index=True);
    teacher_id = Column(Integer, ForeignKey('teachers.id'), unique=True, index=True);
    # users - students - one-to-one (unique) 
    # users - teachers - one-to-one (unique)
    # users - administration - one-to-one (unique)

    student = relationship('Student', back_populates='username');
    admin = relationship('Admin', back_populates='username');
    teacher = relationship('Teacher', back_populates='username');

# -----------------------------------------------------------------
# administrations classes (create, edit, delete permission)
# -----------------------------------------------------------------
class Admin(Base):
    __tablename__ = 'admins';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), unique=True, index=True);
    # users - administration - one-to-one (unique)

    username = relationship('User', back_populates='admin', uselist=False);    

# -----------------------------------------------------------------
# students classes
# -----------------------------------------------------------------
class Student(Base):
    __tablename__ = 'students';

    id = Column(Integer, primary_key=True, index=True);
    last_name = Column(String(255), nullable=False, index=True);
    first_name = Column(String(255), nullable=False, index=True);
    second_name = Column(String(255), index=True);
    academic_year = Column(Integer, ForeignKey('years.number'), index=True);
    academic_group = Column(Integer, ForeignKey('groups.number'), index=True);
    # students - years - many-to-one
    # students - groups - many-to-one
    # users - students - one-to-one (unique)

    year = relationship('AcademicYear', back_populates='students');
    group = relationship('AcademicGroup', back_populates='students');
    username = relationship('User', back_populates='student', uselist=False); 

class AcademicYear(Base):
    __tablename__ = 'years';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, primary_key=True, index=True);
    # students - years - many-to-one

    students = relationship('Student', back_populates='year');

class AcademicGroup(Base):
    __tablename__ = 'groups';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, primary_key=True, index=True);
    # students - groups - many-to-one

    students = relationship('Student', back_populates = 'group');
    schedule = relationship('Schedule', back_populates = 'groups');

class GroupBusy(Base):
    __tablename__ = 'groups_busy';

    id = Column(Integer, primary_key=True, index=True);
    group_id = Column(Integer, nullable=False, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson = Column(Integer, nullable=False, index=True);
    is_busy = Column(Boolean, index=True, default=False);
    
# -----------------------------------------------------------------
# teachers classes
# -----------------------------------------------------------------
teachers_modules = Table(
    'teachers_modules_association', Base.metadata,
    Column('Teacher_id', ForeignKey('teachers.id')),
    Column('Module_id', ForeignKey('modules.id'))
    );


class Teacher(Base):
    __tablename__ = 'teachers';

    id = Column(Integer, primary_key=True, index=True);
    last_name = Column(String(255), nullable=False, index=True);
    first_name = Column(String(255), nullable=False, index=True);
    second_name = Column(String(255), index=True);

    modules = relationship('Module',
                           order_by = 'asc(Module.name)',
                           secondary = teachers_modules,
                           #overlaps = 'teachers',
                           back_populates='teachers');

    username = relationship('User', back_populates = 'teacher', uselist = False);
    schedule = relationship('Schedule', back_populates = 'teachers');

class TeacherBusy(Base):
    __tablename__ = 'teachers_busy';

    id = Column(Integer, primary_key=True, index=True);
    teacher_id = Column(Integer, nullable=False, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson = Column(Integer, nullable=False, index=True);
    is_busy = Column(Boolean, index=True, default=False);
    
# -----------------------------------------------------------------
# modules classes
# -----------------------------------------------------------------
modules_typesOfClasses = Table(
    'modules_typesOfClasses_association', Base.metadata,
    Column('Module_id', ForeignKey('modules.id')),
    Column('TypeOfClass_id', ForeignKey('class_types.id'))
    );

class Module(Base):
    __tablename__ = 'modules';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), nullable=False, index=True);
    year = Column(Integer, nullable=False, index=True);

    classes = relationship('TypeOfClass',
                           order_by = 'asc(TypeOfClass.id)',
                           secondary = modules_typesOfClasses,
                           #overlaps='modules',
                           back_populates='modules');
    
    teachers = relationship('Teacher',
                           order_by = 'asc(Teacher.last_name)',
                           secondary = teachers_modules,
                           #overlaps = 'modules',
                           back_populates='modules');

    schedule = relationship('Schedule', back_populates = 'modules');

class TypeOfClass(Base):
    __tablename__ = 'class_types';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), nullable=False, index=True);
    
    modules = relationship('Module',
                           order_by = 'asc(Module.name)',
                           secondary = modules_typesOfClasses,
                           #overlaps='classes',
                           back_populates='classes');

    # class_type - rooms - one-to-many
    rooms = relationship('Room', back_populates = 'class_type');

    # class_type - schedule - one-to-many
    schedule = relationship('Schedule', back_populates = 'class_types');
    
# -----------------------------------------------------------------
# rooms classes
# -----------------------------------------------------------------
class Room(Base):
    __tablename__ = 'rooms';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, primary_key=True, index=True);
    class_type_id = Column(Integer, ForeignKey('class_types.id'), index=True);
    # class_type - rooms - one-to-many
    # rooms - schedule - one-to-many

    class_type = relationship('TypeOfClass', back_populates = 'rooms');
    schedule = relationship('Schedule', back_populates = 'rooms');

class RoomBusy(Base):
    __tablename__ = 'rooms_busy';

    id = Column(Integer, primary_key=True, index=True);
    room_id = Column(Integer, nullable=False, index=True);
    weekday = Column(String(255), nullable=False, index=True);
    lesson = Column(Integer, nullable=False, index=True);
    is_busy = Column(Boolean, index=True, default=False);

# -----------------------------------------------------------------
# date-time classes
# -----------------------------------------------------------------
weekdays_lessons = Table(
    'weekdays_lessons_association', Base.metadata,
    Column('Weekday_id', ForeignKey('weekdays.id')),
    Column('Lesson_id', ForeignKey('lessons.id'))
    );

class Weekday(Base):
    __tablename__ = 'weekdays';

    id = Column(Integer, primary_key=True, index=True);
    name = Column(String(255), nullable=False, unique=True, index=True);

    lessons = relationship('Lesson',
                           order_by = 'asc(Lesson.id)',
                           secondary = weekdays_lessons,
                           #overlaps='weekdays',
                           back_populates='weekdays');

    schedule = relationship('Schedule', back_populates = 'weekdays');

class Lesson(Base):
    __tablename__ = 'lessons';

    id = Column(Integer, primary_key=True, index=True);
    number = Column(Integer, nullable=False, unique=True, index=True);
    time = Column(String(255), nullable=False, unique=True, index=True);

    weekdays = relationship('Weekday',
                            secondary = weekdays_lessons,
                            #overlaps='lessons',
                            back_populates='lessons');

    schedule = relationship('Schedule', back_populates = 'lessons');
   
# -----------------------------------------------------------------
# semester schedule class 
# -----------------------------------------------------------------
class Schedule(Base):
    __tablename__ = 'schedule';

    id = Column(Integer, primary_key=True, index=True);
    semester = Column(Integer, index=True); 
    group = Column(Integer, ForeignKey('groups.number'), index=True);
    weekday = Column(String(255), ForeignKey('weekdays.name'), nullable=False, index=True);
    lesson_number = Column(Integer, ForeignKey('lessons.number'), nullable=False, index=True);
    module_id = Column(Integer, ForeignKey('modules.id'), index=True);
    class_type = Column(String(255), ForeignKey('class_types.name'),index=True);
    room = Column(Integer, ForeignKey('rooms.number'), index=True);
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False, index=True);

    groups = relationship('AcademicGroup', back_populates = 'schedule');
    weekdays = relationship('Weekday', back_populates = 'schedule');
    lessons = relationship('Lesson', back_populates = 'schedule');
    modules = relationship('Module', back_populates = 'schedule');
    class_types = relationship('TypeOfClass', back_populates = 'schedule');
    rooms = relationship('Room', back_populates = 'schedule');
    teachers = relationship('Teacher', back_populates = 'schedule'); 

