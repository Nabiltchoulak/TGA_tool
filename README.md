# TGA_tool
School management system based on a Django web application

This application is designed to serve as a school management system combined to costumer dedicated interface, for training centers specialized in tutoring or/and language courses. 
## Data structure: 
The application can manage the following:

Students, coaches, courses (activated or can be taught), payments, educational levels, chapters and notions of courses, sessions calendar, sessions validation (by specifying the attendance list and the chapters/notions done in the session) and also a system to register potential costumers requesting not activated courses, those requests can have an end of validation date.

Students are divided into two categories: young student and clients, young student must have at least one parent responsible that will be the holder of an account on the application, giving him access to the costumer interface.

Courses are divided to VIP or group courses; VIP courses are the ones requested by costumer to one person only. The group courses are scheduled by the manager.
## Application usage: 
There are two ways to use the application:
#### 1)	As a school manager:
-	Insert the schedule of courses by creating them and specifying their related information, after that the sessions are automatically created in the calendar on the home page, this will activate the course and let you add students to that course.
-	Register students in the courses.
-	Take different requests.
-	Register coaches.
-	Validate sessions.
-	Create extra session for one course.

#### 2)	As a costumer:
The costumer interface let you do the following:
-	Keep up with the weekly schedule of courses.
-	See the history of payments done.
-	Make course requests directly
-	Follow the courses completion level, and the personal attendance to that course.
-	A family structure gathers costumers from the same family, though if a parent has many young students, he can follow their activity with the same account.

N.B: The application is available only in the French version, an English version is intended in the next releases.
