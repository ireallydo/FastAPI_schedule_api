# schedule_api_fastapi
college schedule API: FastAPI, Pydantic, SQLAlchemy, PostgreSQL

* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker (including Nginx)

<b>included features</b>:
* authorization
* authentication
* access by roles 
* automatic schedule generation
* manual schedule generation with checks


<b>Usage</b>:

<b><i>user registrations</i></b>:
* user with role "admin" can be created with no prerequisites
* to register a user with role "teacher" or "student",
first must have such a student or a teacher created by admin
  (create teacher/student endpoints)
* when admin creates a student/teacher, the registration token
for a student/teacher is created, which should be used during 
registration of user with student/teacher role 

<b><i>academic groups</i></b>: 
* can only use those from the Enums
  (designed that way to )

<b><i>prerequisites to create a schedule</i></b>: 
* lesson created by admin 
* room created by admin (must have a compatible class_type with module)
* module created by admin (must have a compatible class_type with room)
* teacher created by admin 
* teacher assigned to module (create teacher modules endpoint)

