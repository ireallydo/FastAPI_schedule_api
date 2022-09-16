CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> cd330f20026d

CREATE TABLE admins (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(255), 
    PRIMARY KEY (id)
);

CREATE INDEX ix_admins_id ON admins (id);

CREATE UNIQUE INDEX ix_admins_name ON admins (name);

CREATE TABLE class_types (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(255) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_class_types_id ON class_types (id);

CREATE INDEX ix_class_types_name ON class_types (name);

CREATE TABLE `groups` (
    id INTEGER NOT NULL, 
    number INTEGER NOT NULL, 
    PRIMARY KEY (id, number)
);

CREATE INDEX ix_groups_id ON `groups` (id);

CREATE INDEX ix_groups_number ON `groups` (number);

CREATE TABLE groups_busy (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    group_id INTEGER NOT NULL, 
    weekday VARCHAR(255) NOT NULL, 
    lesson INTEGER NOT NULL, 
    is_busy BOOL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_groups_busy_group_id ON groups_busy (group_id);

CREATE INDEX ix_groups_busy_id ON groups_busy (id);

CREATE INDEX ix_groups_busy_is_busy ON groups_busy (is_busy);

CREATE INDEX ix_groups_busy_lesson ON groups_busy (lesson);

CREATE INDEX ix_groups_busy_weekday ON groups_busy (weekday);

CREATE TABLE lessons (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    number INTEGER NOT NULL, 
    time VARCHAR(255) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_lessons_id ON lessons (id);

CREATE UNIQUE INDEX ix_lessons_number ON lessons (number);

CREATE UNIQUE INDEX ix_lessons_time ON lessons (time);

CREATE TABLE modules (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(255) NOT NULL, 
    year INTEGER NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_modules_id ON modules (id);

CREATE INDEX ix_modules_name ON modules (name);

CREATE INDEX ix_modules_year ON modules (year);

CREATE TABLE rooms_busy (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    room_id INTEGER NOT NULL, 
    weekday VARCHAR(255) NOT NULL, 
    lesson INTEGER NOT NULL, 
    is_busy BOOL NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_rooms_busy_id ON rooms_busy (id);

CREATE INDEX ix_rooms_busy_is_busy ON rooms_busy (is_busy);

CREATE INDEX ix_rooms_busy_lesson ON rooms_busy (lesson);

CREATE INDEX ix_rooms_busy_room_id ON rooms_busy (room_id);

CREATE INDEX ix_rooms_busy_weekday ON rooms_busy (weekday);

CREATE TABLE teachers (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    last_name VARCHAR(255) NOT NULL, 
    first_name VARCHAR(255) NOT NULL, 
    second_name VARCHAR(255), 
    PRIMARY KEY (id)
);

CREATE INDEX ix_teachers_first_name ON teachers (first_name);

CREATE INDEX ix_teachers_id ON teachers (id);

CREATE INDEX ix_teachers_last_name ON teachers (last_name);

CREATE INDEX ix_teachers_second_name ON teachers (second_name);

CREATE TABLE teachers_busy (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    teacher_id INTEGER NOT NULL, 
    weekday VARCHAR(255) NOT NULL, 
    lesson INTEGER NOT NULL, 
    is_busy BOOL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_teachers_busy_id ON teachers_busy (id);

CREATE INDEX ix_teachers_busy_is_busy ON teachers_busy (is_busy);

CREATE INDEX ix_teachers_busy_lesson ON teachers_busy (lesson);

CREATE INDEX ix_teachers_busy_teacher_id ON teachers_busy (teacher_id);

CREATE INDEX ix_teachers_busy_weekday ON teachers_busy (weekday);

CREATE TABLE weekdays (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    name VARCHAR(255) NOT NULL, 
    PRIMARY KEY (id)
);

CREATE INDEX ix_weekdays_id ON weekdays (id);

CREATE UNIQUE INDEX ix_weekdays_name ON weekdays (name);

CREATE TABLE years (
    id INTEGER NOT NULL, 
    number INTEGER NOT NULL, 
    PRIMARY KEY (id, number)
);

CREATE INDEX ix_years_id ON years (id);

CREATE INDEX ix_years_number ON years (number);

CREATE TABLE `modules_typesOfClasses_association` (
    `Module_id` INTEGER, 
    `TypeOfClass_id` INTEGER, 
    FOREIGN KEY(`Module_id`) REFERENCES modules (id), 
    FOREIGN KEY(`TypeOfClass_id`) REFERENCES class_types (id)
);

CREATE TABLE rooms (
    id INTEGER NOT NULL, 
    number INTEGER NOT NULL, 
    class_type_id INTEGER, 
    PRIMARY KEY (id, number), 
    FOREIGN KEY(class_type_id) REFERENCES class_types (id)
);

CREATE INDEX ix_rooms_class_type_id ON rooms (class_type_id);

CREATE INDEX ix_rooms_id ON rooms (id);

CREATE INDEX ix_rooms_number ON rooms (number);

CREATE TABLE students (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    last_name VARCHAR(255) NOT NULL, 
    first_name VARCHAR(255) NOT NULL, 
    second_name VARCHAR(255), 
    academic_year INTEGER, 
    academic_group INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(academic_group) REFERENCES `groups` (number), 
    FOREIGN KEY(academic_year) REFERENCES years (number)
);

CREATE INDEX ix_students_academic_group ON students (academic_group);

CREATE INDEX ix_students_academic_year ON students (academic_year);

CREATE INDEX ix_students_first_name ON students (first_name);

CREATE INDEX ix_students_id ON students (id);

CREATE INDEX ix_students_last_name ON students (last_name);

CREATE INDEX ix_students_second_name ON students (second_name);

CREATE TABLE teachers_modules_association (
    `Teacher_id` INTEGER, 
    `Module_id` INTEGER, 
    FOREIGN KEY(`Module_id`) REFERENCES modules (id), 
    FOREIGN KEY(`Teacher_id`) REFERENCES teachers (id)
);

CREATE TABLE weekdays_lessons_association (
    `Weekday_id` INTEGER, 
    `Lesson_id` INTEGER, 
    FOREIGN KEY(`Lesson_id`) REFERENCES lessons (id), 
    FOREIGN KEY(`Weekday_id`) REFERENCES weekdays (id)
);

CREATE TABLE schedule (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    semester INTEGER, 
    `group` INTEGER, 
    weekday VARCHAR(255) NOT NULL, 
    lesson_number INTEGER NOT NULL, 
    module_id INTEGER, 
    class_type VARCHAR(255), 
    room INTEGER, 
    teacher_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(class_type) REFERENCES class_types (name), 
    FOREIGN KEY(`group`) REFERENCES `groups` (number), 
    FOREIGN KEY(lesson_number) REFERENCES lessons (number), 
    FOREIGN KEY(module_id) REFERENCES modules (id), 
    FOREIGN KEY(room) REFERENCES rooms (number), 
    FOREIGN KEY(teacher_id) REFERENCES teachers (id), 
    FOREIGN KEY(weekday) REFERENCES weekdays (name)
);

CREATE INDEX ix_schedule_class_type ON schedule (class_type);

CREATE INDEX ix_schedule_group ON schedule (`group`);

CREATE INDEX ix_schedule_id ON schedule (id);

CREATE INDEX ix_schedule_lesson_number ON schedule (lesson_number);

CREATE INDEX ix_schedule_module_id ON schedule (module_id);

CREATE INDEX ix_schedule_room ON schedule (room);

CREATE INDEX ix_schedule_semester ON schedule (semester);

CREATE INDEX ix_schedule_teacher_id ON schedule (teacher_id);

CREATE INDEX ix_schedule_weekday ON schedule (weekday);

CREATE TABLE users (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    username VARCHAR(255), 
    email VARCHAR(255), 
    hashed_password VARCHAR(255), 
    is_active BOOL, 
    student_id INTEGER, 
    admin_id INTEGER, 
    teacher_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(admin_id) REFERENCES admins (id), 
    FOREIGN KEY(student_id) REFERENCES students (id), 
    FOREIGN KEY(teacher_id) REFERENCES teachers (id)
);

CREATE UNIQUE INDEX ix_users_admin_id ON users (admin_id);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE INDEX ix_users_id ON users (id);

CREATE UNIQUE INDEX ix_users_student_id ON users (student_id);

CREATE UNIQUE INDEX ix_users_teacher_id ON users (teacher_id);

CREATE UNIQUE INDEX ix_users_username ON users (username);

INSERT INTO alembic_version (version_num) VALUES ('cd330f20026d');

-- Running upgrade cd330f20026d -> 38ecca09181c

ALTER TABLE users ADD COLUMN test_alembic INTEGER;

UPDATE alembic_version SET version_num='38ecca09181c' WHERE alembic_version.version_num = 'cd330f20026d';

