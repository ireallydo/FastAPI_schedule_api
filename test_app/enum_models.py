from enum import Enum;

class Weekdays(str, Enum):
    one = 'Monday';
    two = 'Tuesday';
    three = 'Wednesday';
    four = 'Thursday';
    five = 'Friday';

class Lessons(str, Enum):
    one = 1;
    two = 2;
    three = 3;

class ClassTypes(str, Enum):
    one = 'lecture';
    two = 'seminar';
    three = 'laboratory';

class Semesters(str, Enum):
    one = 1;
    two = 2;
    

#print(Weekdays('Monday').name);

print(Semesters.one);

a = '1';

print(type(int(a)));
