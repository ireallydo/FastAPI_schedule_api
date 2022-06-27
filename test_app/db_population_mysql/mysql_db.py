import mysql.connector;

mydb = mysql.connector.connect(
    host='localhost',
    user='superuser',
    password='password',
    database='test1'
    );

mycursor = mydb.cursor();

phnull = None;

### ---------------------------------------
### CREATE DATABASE
### ---------------------------------------
##
### mycursor.execute('CREATE DATABASE test1');
##
# ---------------------------------------
# POPULATE YEARS TABLE
# ---------------------------------------

##sql = 'INSERT INTO years (id, number) VALUES (%s, %s)';
##val = [
##    (1,1),
##    (2,2),
##    (3,3)
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);
##
##print('----------\nYEARS TABLE\n----------');
##mycursor.execute('SELECT * FROM years');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x); 

# ---------------------------------------
# POPULATE GROUPS TABLE
# ---------------------------------------

##sql = 'INSERT INTO `groups` (id, number) VALUES (%s, %s)';
##val = [
##    (1,11),
##    (2,12),
##    (3,21),
##    (4,22),
##    (5,31),
##    (6,32)
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);
##
##print('----------\nGROUPS TABLE\n----------');
##mycursor.execute('SELECT * FROM `groups`');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);
##    
# ---------------------------------------
# POPULATE WEEKDAYS TABLE
# ---------------------------------------

##sql = 'INSERT INTO weekdays VALUES(%s,%s)'
##val = [
##    (1,"Понедельник"),
##    (2,"Вторник"),
##    (3,"Среда"),
##    (4,"Четверг"),
##    (5,"Пятница")
##    ]
##
##mycursor.executemany(sql, val);
##
##mydb.commit();
##
##print(mycursor.rowcount, 'were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nWEEKDAYS TABLE\n----------');
##mycursor.execute('SELECT * FROM weekdays order by id asc');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x); 

# ---------------------------------------
# POPULATE LESSONS TABLE
# ---------------------------------------

##sql = 'INSERT INTO lessons VALUES(%s, %s, %s)'
##val = [
##    (1,1,'8:30-10:10'),
##    (2,2,'10:30-12:10'),
##    (3,3,'12:30-14:10')
##    ]
##
##mycursor.executemany(sql,val);
##mydb.commit();
##
##print(mycursor.rowcount, 'were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nLESSONS TABLE\n----------');
##mycursor.execute('SELECT * FROM lessons');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x); 
### ---------------------------------------
##
##
# ---------------------------------------
# POPULATE WEEKDAYS_LESONS ASSOCIATION TABLE
# ---------------------------------------

##sql = 'INSERT INTO weekdays_lessons_association VALUES (%s, %s)';
##val = [
##    (1,1),(1,2),(1,3),
##    (2,1),(2,2),(2,3),
##    (3,1),(3,2),(3,3),
##    (4,1),(4,2),(4,3),
##    (5,1),(5,2),(5,3),
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, 'were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nweekdays_lessons_association TABLE\n----------');
##mycursor.execute('SELECT * FROM weekdays_lessons_association');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);
##
### ---------------------------------------
##
##
# ---------------------------------------
# POPULATE GROUPS_BUSY TABLE
# ---------------------------------------

sql = 'INSERT INTO groups_busy (group_id, weekday, lesson, is_busy) VALUES (%s, %s, %s, %s)';
val = [
    (1, "Понедельник", 1, False),
    (1, "Понедельник", 2, False),
    (1, "Понедельник", 3, False),
    (1,"Вторник", 1, False),
    (1,"Вторник", 2, False),
    (1,"Вторник", 3, False),
    (1, "Среда", 1, False),
    (1, "Среда", 2, False),
    (1, "Среда", 3, False),
    (1, "Четверг", 1, False),
    (1, "Четверг", 2, False),
    (1, "Четверг", 3, False),
    (1, "Пятница", 1, False),
    (1, "Пятница", 2, False),
    (1, "Пятница", 3, False),

    (2, "Понедельник", 1, False),
    (2, "Понедельник", 2, False),
    (2, "Понедельник", 3, False),
    (2,"Вторник", 1, False),
    (2,"Вторник", 2, False),
    (2,"Вторник", 3, False),
    (2, "Среда", 1, False),
    (2, "Среда", 2, False),
    (2, "Среда", 3, False),
    (2, "Четверг", 1, False),
    (2, "Четверг", 2, False),
    (2, "Четверг", 3, False),
    (2, "Пятница", 1, False),
    (2, "Пятница", 2, False),
    (2, "Пятница", 3, False),

    (3, "Понедельник", 1, False),
    (3, "Понедельник", 2, False),
    (3, "Понедельник", 3, False),
    (3,"Вторник", 1, False),
    (3,"Вторник", 2, False),
    (3,"Вторник", 3, False),
    (3, "Среда", 1, False),
    (3, "Среда", 2, False),
    (3, "Среда", 3, False),
    (3, "Четверг", 1, False),
    (3, "Четверг", 2, False),
    (3, "Четверг", 3, False),
    (3, "Пятница", 1, False),
    (3, "Пятница", 2, False),
    (3, "Пятница", 3, False),

    (4, "Понедельник", 1, False),
    (4, "Понедельник", 2, False),
    (4, "Понедельник", 3, False),
    (4,"Вторник", 1, False),
    (4,"Вторник", 2, False),
    (4,"Вторник", 3, False),
    (4, "Среда", 1, False),
    (4, "Среда", 2, False),
    (4, "Среда", 3, False),
    (4, "Четверг", 1, False),
    (4, "Четверг", 2, False),
    (4, "Четверг", 3, False),
    (4, "Пятница", 1, False),
    (4, "Пятница", 2, False),
    (4, "Пятница", 3, False),

    (5, "Понедельник", 1, False),
    (5, "Понедельник", 2, False),
    (5, "Понедельник", 3, False),
    (5,"Вторник", 1, False),
    (5,"Вторник", 2, False),
    (5,"Вторник", 3, False),
    (5, "Среда", 1, False),
    (5, "Среда", 2, False),
    (5, "Среда", 3, False),
    (5, "Четверг", 1, False),
    (5, "Четверг", 2, False),
    (5, "Четверг", 3, False),
    (5, "Пятница", 1, False),
    (5, "Пятница", 2, False),
    (5, "Пятница", 3, False),

    (6, "Понедельник", 1, False),
    (6, "Понедельник", 2, False),
    (6, "Понедельник", 3, False),
    (6,"Вторник", 1, False),
    (6,"Вторник", 2, False),
    (6,"Вторник", 3, False),
    (6, "Среда", 1, False),
    (6, "Среда", 2, False),
    (6, "Среда", 3, False),
    (6, "Четверг", 1, False),
    (6, "Четверг", 2, False),
    (6, "Четверг", 3, False),
    (6, "Пятница", 1, False),
    (6, "Пятница", 2, False),
    (6, "Пятница", 3, False),
    ];

mycursor.executemany(sql,val);
mydb.commit();
print(mycursor.rowcount, ' rows were inserted');
print('last row id:', mycursor.lastrowid);


print('----------\ngroups_busy TABLE\n----------');
mycursor.execute('SELECT * FROM groups_busy');
myresult = mycursor.fetchall();
for x in myresult:
    print(x);
##
### ---------------------------------------
### POPULATE ADMINS TABLE
### ---------------------------------------

##sql = 'INSERT INTO admins(id, name) VALUES (%s,%s)';
##val = [
##    (1,'Carl'),
##    (2,'Clara'),
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nADMINS TABLE\n----------');
##mycursor.execute('SELECT * FROM admins');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);

### ---------------------------------------
### POPULATE STUDENTS TABLE
### ---------------------------------------

##sql = 'INSERT INTO students (last_name, first_name, second_name, academic_year, academic_group) VALUES (%s, %s, %s, %s, %s)';
##val = [
##    ('Иванова','Агриппина','Петровна',1,11),
##    ('Валялькин','Иван','Шурикович',1,11),
##    ('Руссо','Жан Жак', phnull,1,12),
##    ('Бикмуллин','Шерзод', phnull,1,12),
##    ('Петрова','Агриппина','Петровна',2,21),
##    ('Салочкина','Анна','Валерьевна',2,21),
##    ('Корнеев','Корней', phnull,2,22),
##    ('Саночкин','Эдуард','Эдуардович',2,22),
##    ('Белочка','Зоя','Яковлевна',3,31),
##    ('Берия','Марат','Виноградович',3,31),
##    ('Колик','Валентина','Шеукетовна',3,32),
##    ('Руссо','Жан Жак', phnull,3,32),
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nSTUDENTS TABLE\n----------');
##mycursor.execute('SELECT * FROM students');
##result = mycursor.fetchall();
##for x in result:
##    print(x); 

# ---------------------------------------
# POPULATE TEACHERS TABLE
# ---------------------------------------
##
##sql = 'INSERT INTO teachers (last_name, first_name, second_name) VALUES  (%s, %s, %s)';
##val = [
##    # недоступные проблемы
##    ('Ойра-Ойра','Роман','Петрович'),
##    ('Почкин','Владимир', phnull),
##    # универсальные превращения
##    ('Корнеев','Виктор','Павлович'),
##    ('Жиакомо','Жиан', phnull),
##    # линейное счастье
##    ('Амперян','Эдуард', phnull),
##    # абсолютное знание
##    ('Пупков-Задний','Морис-Иоганн-Лаврентий', phnull),
##    ('Седловой','Луи','Иванович'),
##    # социальная метеорология
##    ('Выбегалло','Амвросий','Амбруазович'),
##    ('Редькин','Магнус','Федорович'),
##    ('Бальзамо','Джузеппе', phnull),
##    # воинствующий атеизм 
##    ('Неунывай-Дубино','Перун','Маркович'),
##    # математический анализ
##    ('Привалов','Александр', 'Иванович')
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);
##
##print('----------\nTEACHERS TABLE\n----------');
##mycursor.execute('SELECT * FROM teachers');
##result = mycursor.fetchall();
##for x in result:
##    print(x); 

# ---------------------------------------
# POPULATE TEACHERS_BUSY TABLE
# ---------------------------------------

sql = 'INSERT INTO teachers_busy (teacher_id, weekday, lesson, is_busy) VALUES (%s,%s, %s, %s)';
val = [
    (1, "Понедельник", 1, False),
    (1, "Понедельник", 2, False),
    (1, "Понедельник", 3, False),
    (1,"Вторник", 1, False),
    (1,"Вторник", 2, False),
    (1,"Вторник", 3, False),
    (1, "Среда", 1, False),
    (1, "Среда", 2, False),
    (1, "Среда", 3, False),
    (1, "Четверг", 1, False),
    (1, "Четверг", 2, False),
    (1, "Четверг", 3, False),
    (1, "Пятница", 1, False),
    (1, "Пятница", 2, False),
    (1, "Пятница", 3, False),

    (2, "Понедельник", 1, False),
    (2, "Понедельник", 2, False),
    (2, "Понедельник", 3, False),
    (2,"Вторник", 1, False),
    (2,"Вторник", 2, False),
    (2,"Вторник", 3, False),
    (2, "Среда", 1, False),
    (2, "Среда", 2, False),
    (2, "Среда", 3, False),
    (2, "Четверг", 1, False),
    (2, "Четверг", 2, False),
    (2, "Четверг", 3, False),
    (2, "Пятница", 1, False),
    (2, "Пятница", 2, False),
    (2, "Пятница", 3, False),

    (3, "Понедельник", 1, False),
    (3, "Понедельник", 2, False),
    (3, "Понедельник", 3, False),
    (3,"Вторник", 1, False),
    (3,"Вторник", 2, False),
    (3,"Вторник", 3, False),
    (3, "Среда", 1, False),
    (3, "Среда", 2, False),
    (3, "Среда", 3, False),
    (3, "Четверг", 1, False),
    (3, "Четверг", 2, False),
    (3, "Четверг", 3, False),
    (3, "Пятница", 1, False),
    (3, "Пятница", 2, False),
    (3, "Пятница", 3, False),

    (4, "Понедельник", 1, False),
    (4, "Понедельник", 2, False),
    (4, "Понедельник", 3, False),
    (4,"Вторник", 1, False),
    (4,"Вторник", 2, False),
    (4,"Вторник", 3, False),
    (4, "Среда", 1, False),
    (4, "Среда", 2, False),
    (4, "Среда", 3, False),
    (4, "Четверг", 1, False),
    (4, "Четверг", 2, False),
    (4, "Четверг", 3, False),
    (4, "Пятница", 1, False),
    (4, "Пятница", 2, False),
    (4, "Пятница", 3, False),

    (5, "Понедельник", 1, False),
    (5, "Понедельник", 2, False),
    (5, "Понедельник", 3, False),
    (5,"Вторник", 1, False),
    (5,"Вторник", 2, False),
    (5,"Вторник", 3, False),
    (5, "Среда", 1, False),
    (5, "Среда", 2, False),
    (5, "Среда", 3, False),
    (5, "Четверг", 1, False),
    (5, "Четверг", 2, False),
    (5, "Четверг", 3, False),
    (5, "Пятница", 1, False),
    (5, "Пятница", 2, False),
    (5, "Пятница", 3, False),

    (6, "Понедельник", 1, False),
    (6, "Понедельник", 2, False),
    (6, "Понедельник", 3, False),
    (6,"Вторник", 1, False),
    (6,"Вторник", 2, False),
    (6,"Вторник", 3, False),
    (6, "Среда", 1, False),
    (6, "Среда", 2, False),
    (6, "Среда", 3, False),
    (6, "Четверг", 1, False),
    (6, "Четверг", 2, False),
    (6, "Четверг", 3, False),
    (6, "Пятница", 1, False),
    (6, "Пятница", 2, False),
    (6, "Пятница", 3, False),

    (7, "Понедельник", 1, False),
    (7, "Понедельник", 2, False),
    (7, "Понедельник", 3, False),
    (7,"Вторник", 1, False),
    (7,"Вторник", 2, False),
    (7,"Вторник", 3, False),
    (7, "Среда", 1, False),
    (7, "Среда", 2, False),
    (7, "Среда", 3, False),
    (7, "Четверг", 1, False),
    (7, "Четверг", 2, False),
    (7, "Четверг", 3, False),
    (7, "Пятница", 1, False),
    (7, "Пятница", 2, False),
    (7, "Пятница", 3, False),

    (8, "Понедельник", 1, False),
    (8, "Понедельник", 2, False),
    (8, "Понедельник", 3, False),
    (8,"Вторник", 1, False),
    (8,"Вторник", 2, False),
    (8,"Вторник", 3, False),
    (8, "Среда", 1, False),
    (8, "Среда", 2, False),
    (8, "Среда", 3, False),
    (8, "Четверг", 1, False),
    (8, "Четверг", 2, False),
    (8, "Четверг", 3, False),
    (8, "Пятница", 1, False),
    (8, "Пятница", 2, False),
    (8, "Пятница", 3, False),

    (9, "Понедельник", 1, False),
    (9, "Понедельник", 2, False),
    (9, "Понедельник", 3, False),
    (9,"Вторник", 1, False),
    (9,"Вторник", 2, False),
    (9,"Вторник", 3, False),
    (9, "Среда", 1, False),
    (9, "Среда", 2, False),
    (9, "Среда", 3, False),
    (9, "Четверг", 1, False),
    (9, "Четверг", 2, False),
    (9, "Четверг", 3, False),
    (9, "Пятница", 1, False),
    (9, "Пятница", 2, False),
    (9, "Пятница", 3, False),

    (10, "Понедельник", 1, False),
    (10, "Понедельник", 2, False),
    (10, "Понедельник", 3, False),
    (10,"Вторник", 1, False),
    (10,"Вторник", 2, False),
    (10,"Вторник", 3, False),
    (10, "Среда", 1, False),
    (10, "Среда", 2, False),
    (10, "Среда", 3, False),
    (10, "Четверг", 1, False),
    (10, "Четверг", 2, False),
    (10, "Четверг", 3, False),
    (10, "Пятница", 1, False),
    (10, "Пятница", 2, False),
    (10, "Пятница", 3, False),

    (11, "Понедельник", 1, False),
    (11, "Понедельник", 2, False),
    (11, "Понедельник", 3, False),
    (11,"Вторник", 1, False),
    (11,"Вторник", 2, False),
    (11,"Вторник", 3, False),
    (11, "Среда", 1, False),
    (11, "Среда", 2, False),
    (11, "Среда", 3, False),
    (11, "Четверг", 1, False),
    (11, "Четверг", 2, False),
    (11, "Четверг", 3, False),
    (11, "Пятница", 1, False),
    (11, "Пятница", 2, False),
    (11, "Пятница", 3, False),

    (12, "Понедельник", 1, False),
    (12, "Понедельник", 2, False),
    (12, "Понедельник", 3, False),
    (12,"Вторник", 1, False),
    (12,"Вторник", 2, False),
    (12,"Вторник", 3, False),
    (12, "Среда", 1, False),
    (12, "Среда", 2, False),
    (12, "Среда", 3, False),
    (12, "Четверг", 1, False),
    (12, "Четверг", 2, False),
    (12, "Четверг", 3, False),
    (12, "Пятница", 1, False),
    (12, "Пятница", 2, False),
    (12, "Пятница", 3, False),
    ];

mycursor.executemany(sql,val);
mydb.commit();
print(mycursor.rowcount, ' rows were inserted');
print('last row id:', mycursor.lastrowid);

print('----------\nteachers_busy TABLE\n----------');
mycursor.execute('SELECT * FROM teachers_busy');
myresult = mycursor.fetchall();
for x in myresult:
    print(x);
##
### ---------------------------------------
### POPULATE MODULES TABLE
### ---------------------------------------
##
##sql = 'INSERT INTO modules (name, year) VALUES  (%s, %s)';
##val = [
##    ("Недоступные Проблемы", 1), #1
##    ("Универсальные Превращения, ч.1", 1), #2
##    ("Линейное Счастье, ч.1", 1), #3
##    ("Математический Анализ, ч.1", 1), #4
##    ("Социальная Метеорология, ч.1", 1), #5
##    ("Линейное Счастье, ч.2", 2), #6
##    ("Математический Анализ, ч.2", 2), #7
##    ("Социальная Метеорология, ч.2", 2), #8
##    ("Воинствующий Атеизм, ч.1", 2), #9
##    ("Матрицы и Ложки, ч.1", 2), #10
##    ("Универсальные Превращения, ч.2", 2), #11
##    ("Универсальные Превращения, ч.3", 3), #12
##    ("Линейное Счастье, ч.3", 3), #13
##    ("Абсолютное Знание", 3), #14
##    ("Матрицы и Ложки, ч.2", 3), #15
##    ("Воинствующий Атеизм, ч.2", 3) #16
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nMODULES TABLE\n----------');
##mycursor.execute('SELECT * FROM modules');
##result = mycursor.fetchall();
##for x in result:
##    print(x); 
##
##
# ---------------------------------------
# POPULATE TEACHERS_MODULES ASSOCIATION TABLE
# ---------------------------------------

##sql = 'INSERT INTO teachers_modules_association VALUES (%s, %s)';
##val = [
##    (1,1),
##    (2,1),
##    (3,2), (3,11), (3,12),
##    (4,2), (4,11), (4,12),
##    (5,3), (5,6), (5,13),
##    (6,14),
##    (7,14),
##    (8,5), (8,8),
##    (9,5), (9,8),
##    (10,5), (10,8),
##    (11,9), (11,16),
##    (12,4), (12,7), (12,10), (12,15)
##    ];
##
##
####    # недоступные проблемы 1
####    1('Ойра-Ойра','Роман','Петрович'),
####    2('Почкин','Владимир', phnull),
####    # универсальные превращения 2, 11, 12
####    3('Корнеев','Виктор','Павлович'),
####    4('Жиакомо','Жиан', phnull),
####    # линейное счастье 3, 6, 13
####    5('Амперян','Эдуард', phnull),
####    # абсолютное знание 14
####    6('Пупков-Задний','Морис-Иоганн-Лаврентий', phnull),
####    7('Седловой','Луи','Иванович'),
####    # социальная метеорология 5,8
####    8('Выбегалло','Амвросий','Амбруазович'),
####    9('Редькин','Магнус','Федорович'),
####    10('Бальзамо','Джузеппе', phnull),
####    # воинствующий атеизм 9, 16
####    11('Неунывай-Дубино','Перун','Маркович'),
####    # математический анализ 4,7
####    # матрицы и ложки 10, 15
####    12('Привалов','Александр', 'Иванович')
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, 'were inserted');
##print('last row id:', mycursor.lastrowid);
##
##print('----------\nteachers_modules_association TABLE\n----------');
##mycursor.execute('SELECT * FROM teachers_modules_association');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);

### ---------------------------------------
### POPULATE class_types TABLE
### ---------------------------------------
##
##sql = 'INSERT INTO class_types(id,name) VALUES (%s,%s)';
##val = [
##    (1,'лк'),
##    (2,'сем'),
##    (3,'лаб')
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nclass_types TABLE\n----------');
##mycursor.execute('SELECT * FROM class_types');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);

### ---------------------------------------
### POPULATE MODULES_TYPESofCLASSES ASSOCIATION TABLE
### ---------------------------------------
##
##sql = 'INSERT INTO modules_typesOfClasses_association VALUES (%s, %s)';
##val = [
##    (1,1), (1,2),
##    (2,3),
##    (3,1),
##    (4,1), (4,2),
##    (5,1), (5,3),
##    (6,1),
##    (7,1), (7,2),
##    (8,1), (8,3),
##    (9,2),
##    (10,1), (10,3),
##    (11,3), 
##    (12,3),
##    (13,3),
##    (14,1),
##    (15,1), (15,3),
##    (16,3)
##    ];
##
####    ("Недоступные Проблемы", 1), #1 - 1,2
####    ("Универсальные Превращения, ч.1", 1), #2 - 3
####    ("Линейное Счастье, ч.1", 1), #3 - 1
####    ("Математический Анализ, ч.1", 1), #4 - 1,2
####    ("Социальная Метеорология, ч.1", 1), #5 - 1,3
####    ("Линейное Счастье, ч.2", 2), #6 - 1
####    ("Математический Анализ, ч.2", 2), #7 - 1,2
####    ("Социальная Метеорология, ч.2", 2), #8 - 1,3
####    ("Воинствующий Атеизм, ч.1", 2), #9 - 2
####    ("Матрицы и Ложки, ч.1", 2), #10 - 1,3
####    ("Универсальные Превращения, ч.2", 2), #11 - 3
####    ("Универсальные Превращения, ч.3", 3), #12 - 3
####    ("Линейное Счастье, ч.3", 3), #13 - 3
####    ("Абсолютное Знание", 3), #14 - 1
####    ("Матрицы и Ложки, ч.2", 3), #15 - 1,3
####    ("Воинствующий Атеизм, ч.2", 3) #16 - 3
##
##
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, 'were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nmodules_typesOfClasses_association TABLE\n----------');
##mycursor.execute('SELECT * FROM modules_typesOfClasses_association');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);


### ---------------------------------------
### POPULATE ROOMS TABLE
### ---------------------------------------

##sql = 'INSERT INTO rooms (id, number, class_type_id) VALUES  (%s,%s, %s)';
##val = [
##    (1, 101, 1), (2, 102, 1), (3, 103, 1), (4, 104, 1),
##    (5, 201, 2), (6, 202, 2), (7, 203, 2), (8, 204, 2),
##    (9, 301, 3), (10, 302, 3), (11, 303, 3), (12, 304, 3)
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nROOMS TABLE\n----------');
##mycursor.execute('SELECT * FROM rooms');
##result = mycursor.fetchall();
##for x in result:
##    print(x); 

# ---------------------------------------
# POPULATE ROOMS_BUSY TABLE
# ---------------------------------------

##sql = 'INSERT INTO rooms_busy (room_id, weekday, lesson, is_busy) VALUES (%s,%s, %s, %s)';
##val = [
##    (1, "Понедельник", 1, False),
##    (1, "Понедельник", 2, False),
##    (1, "Понедельник", 3, False),
##    (1,"Вторник", 1, False),
##    (1,"Вторник", 2, False),
##    (1,"Вторник", 3, False),
##    (1, "Среда", 1, False),
##    (1, "Среда", 2, False),
##    (1, "Среда", 3, False),
##    (1, "Четверг", 1, False),
##    (1, "Четверг", 2, False),
##    (1, "Четверг", 3, False),
##    (1, "Пятница", 1, False),
##    (1, "Пятница", 2, False),
##    (1, "Пятница", 3, False),
##
##    (2, "Понедельник", 1, False),
##    (2, "Понедельник", 2, False),
##    (2, "Понедельник", 3, False),
##    (2,"Вторник", 1, False),
##    (2,"Вторник", 2, False),
##    (2,"Вторник", 3, False),
##    (2, "Среда", 1, False),
##    (2, "Среда", 2, False),
##    (2, "Среда", 3, False),
##    (2, "Четверг", 1, False),
##    (2, "Четверг", 2, False),
##    (2, "Четверг", 3, False),
##    (2, "Пятница", 1, False),
##    (2, "Пятница", 2, False),
##    (2, "Пятница", 3, False),
##
##    (3, "Понедельник", 1, False),
##    (3, "Понедельник", 2, False),
##    (3, "Понедельник", 3, False),
##    (3,"Вторник", 1, False),
##    (3,"Вторник", 2, False),
##    (3,"Вторник", 3, False),
##    (3, "Среда", 1, False),
##    (3, "Среда", 2, False),
##    (3, "Среда", 3, False),
##    (3, "Четверг", 1, False),
##    (3, "Четверг", 2, False),
##    (3, "Четверг", 3, False),
##    (3, "Пятница", 1, False),
##    (3, "Пятница", 2, False),
##    (3, "Пятница", 3, False),
##
##    (4, "Понедельник", 1, False),
##    (4, "Понедельник", 2, False),
##    (4, "Понедельник", 3, False),
##    (4,"Вторник", 1, False),
##    (4,"Вторник", 2, False),
##    (4,"Вторник", 3, False),
##    (4, "Среда", 1, False),
##    (4, "Среда", 2, False),
##    (4, "Среда", 3, False),
##    (4, "Четверг", 1, False),
##    (4, "Четверг", 2, False),
##    (4, "Четверг", 3, False),
##    (4, "Пятница", 1, False),
##    (4, "Пятница", 2, False),
##    (4, "Пятница", 3, False),
##
##    (5, "Понедельник", 1, False),
##    (5, "Понедельник", 2, False),
##    (5, "Понедельник", 3, False),
##    (5,"Вторник", 1, False),
##    (5,"Вторник", 2, False),
##    (5,"Вторник", 3, False),
##    (5, "Среда", 1, False),
##    (5, "Среда", 2, False),
##    (5, "Среда", 3, False),
##    (5, "Четверг", 1, False),
##    (5, "Четверг", 2, False),
##    (5, "Четверг", 3, False),
##    (5, "Пятница", 1, False),
##    (5, "Пятница", 2, False),
##    (5, "Пятница", 3, False),
##
##    (6, "Понедельник", 1, False),
##    (6, "Понедельник", 2, False),
##    (6, "Понедельник", 3, False),
##    (6,"Вторник", 1, False),
##    (6,"Вторник", 2, False),
##    (6,"Вторник", 3, False),
##    (6, "Среда", 1, False),
##    (6, "Среда", 2, False),
##    (6, "Среда", 3, False),
##    (6, "Четверг", 1, False),
##    (6, "Четверг", 2, False),
##    (6, "Четверг", 3, False),
##    (6, "Пятница", 1, False),
##    (6, "Пятница", 2, False),
##    (6, "Пятница", 3, False),
##
##    (7, "Понедельник", 1, False),
##    (7, "Понедельник", 2, False),
##    (7, "Понедельник", 3, False),
##    (7,"Вторник", 1, False),
##    (7,"Вторник", 2, False),
##    (7,"Вторник", 3, False),
##    (7, "Среда", 1, False),
##    (7, "Среда", 2, False),
##    (7, "Среда", 3, False),
##    (7, "Четверг", 1, False),
##    (7, "Четверг", 2, False),
##    (7, "Четверг", 3, False),
##    (7, "Пятница", 1, False),
##    (7, "Пятница", 2, False),
##    (7, "Пятница", 3, False),
##
##    (8, "Понедельник", 1, False),
##    (8, "Понедельник", 2, False),
##    (8, "Понедельник", 3, False),
##    (8,"Вторник", 1, False),
##    (8,"Вторник", 2, False),
##    (8,"Вторник", 3, False),
##    (8, "Среда", 1, False),
##    (8, "Среда", 2, False),
##    (8, "Среда", 3, False),
##    (8, "Четверг", 1, False),
##    (8, "Четверг", 2, False),
##    (8, "Четверг", 3, False),
##    (8, "Пятница", 1, False),
##    (8, "Пятница", 2, False),
##    (8, "Пятница", 3, False),
##
##    (9, "Понедельник", 1, False),
##    (9, "Понедельник", 2, False),
##    (9, "Понедельник", 3, False),
##    (9,"Вторник", 1, False),
##    (9,"Вторник", 2, False),
##    (9,"Вторник", 3, False),
##    (9, "Среда", 1, False),
##    (9, "Среда", 2, False),
##    (9, "Среда", 3, False),
##    (9, "Четверг", 1, False),
##    (9, "Четверг", 2, False),
##    (9, "Четверг", 3, False),
##    (9, "Пятница", 1, False),
##    (9, "Пятница", 2, False),
##    (9, "Пятница", 3, False),
##
##    (10, "Понедельник", 1, False),
##    (10, "Понедельник", 2, False),
##    (10, "Понедельник", 3, False),
##    (10,"Вторник", 1, False),
##    (10,"Вторник", 2, False),
##    (10,"Вторник", 3, False),
##    (10, "Среда", 1, False),
##    (10, "Среда", 2, False),
##    (10, "Среда", 3, False),
##    (10, "Четверг", 1, False),
##    (10, "Четверг", 2, False),
##    (10, "Четверг", 3, False),
##    (10, "Пятница", 1, False),
##    (10, "Пятница", 2, False),
##    (10, "Пятница", 3, False),
##
##    (11, "Понедельник", 1, False),
##    (11, "Понедельник", 2, False),
##    (11, "Понедельник", 3, False),
##    (11,"Вторник", 1, False),
##    (11,"Вторник", 2, False),
##    (11,"Вторник", 3, False),
##    (11, "Среда", 1, False),
##    (11, "Среда", 2, False),
##    (11, "Среда", 3, False),
##    (11, "Четверг", 1, False),
##    (11, "Четверг", 2, False),
##    (11, "Четверг", 3, False),
##    (11, "Пятница", 1, False),
##    (11, "Пятница", 2, False),
##    (11, "Пятница", 3, False),
##
##    (12, "Понедельник", 1, False),
##    (12, "Понедельник", 2, False),
##    (12, "Понедельник", 3, False),
##    (12,"Вторник", 1, False),
##    (12,"Вторник", 2, False),
##    (12,"Вторник", 3, False),
##    (12, "Среда", 1, False),
##    (12, "Среда", 2, False),
##    (12, "Среда", 3, False),
##    (12, "Четверг", 1, False),
##    (12, "Четверг", 2, False),
##    (12, "Четверг", 3, False),
##    (12, "Пятница", 1, False),
##    (12, "Пятница", 2, False),
##    (12, "Пятница", 3, False),
##    ];
##
##mycursor.executemany(sql,val);
##mydb.commit();
##print(mycursor.rowcount, ' rows were inserted');
##print('last row id:', mycursor.lastrowid);

##print('----------\nteachers_busy TABLE\n----------');
##mycursor.execute('SELECT * FROM rooms_busy');
##myresult = mycursor.fetchall();
##for x in myresult:
##    print(x);







##
##
### --- template ---- 
##
##
####sql = 'INSERT INTO () VALUES ()';
####val = [
####    ()
####    ];
####
####mycursor.executemany(sql,val);
####mydb.commit();
####print(mycursor.rowcount, ' rows were inserted');
####print('last row id:', mycursor.lastrowid);
##
##
##
##
##
##
### ---------------------------------------
### POPULATE USERS TABLE
### ---------------------------------------
##
####sql = 'INSERT INTO users (username, email, full_name, hashed_password, disabled) VALUES (%s, %s, %s, %s, %s)';
####val = [
####    ('johndoe', 'johndoe@example.com', 'John Doe', 'fakehashedpassword1', False),
####    ('alice', 'alice@example.com', 'Alice What', 'fakehashedpassword2', True)
####    ];
####
####mycursor.executemany(sql,val);
####mydb.commit();
####print(mycursor.rowcount, 'were inserted');
####print(mycursor.lastrowid);
####
####mycursor.execute('SELECT * FROM users');
####myresult = mycursor.fetchall();
####for x in myresult:
####    print(x);
##
### ---------------------------------------
