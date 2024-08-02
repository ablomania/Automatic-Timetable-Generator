from .models import Course, Timetable, UserAccount, Location,ExamSchedule, Department , College, Lecturer
import random


def generateExamsTable(course_id, user_id, timetable_id):
    current_course = Course.objects.get(id=course_id)
    locations = getLocation(course=current_course, user_id=user_id, timetable_id=timetable_id)
    print("f1")
    day = getDay(course=current_course, user_id=user_id, timetable_id=timetable_id)
    print("f2")
    getTime(locations=locations, day=day, course=current_course, timetable_id=timetable_id, user_id=user_id)


def getLocation(course, user_id, timetable_id,):
    exam_size = course.exam_size
    if exam_size > 0: pass
    else: exam_size = 100
    locations = Location.objects.filter(creator_id=user_id)
    course_capacity = course.estimated_class_size
    locations = list(dict(locations.filter(creator_id=user_id).values_list("id", "name")))
    factor = course_capacity // exam_size
    if (course_capacity % exam_size) == 0: pass
    elif(course_capacity % exam_size) < 10: pass
    else: factor = factor + 1
    location_list = []
    isDone = 0
    while len(location_list) < factor:
        randnum = random.choice(locations)
        location_list.append(randnum)
        locations.remove(randnum)
    return location_list

def getDay(course, user_id, timetable_id):
    department = Department.objects.get(id=course.department_id)
    college = College.objects.get(id=department.college_main_id)
    check_day = ExamSchedule.objects.filter(creator_id=user_id)
    check_day2 = list(dict(ExamSchedule.objects.filter(creator_id=user_id, department_id=department.id, year_group=course.year_group, timetable_id=timetable_id).values_list("day", "id")))
    all_days = [i for i in range(1, college.exam_days+1)]
    for day in list(all_days):
        if day in list(check_day2): all_days.remove(day)
        else: pass
    for day in list(all_days):
        if day % 2 == 0: all_days.remove(day)
    rand_day = random.choice(all_days)
    return rand_day

def getTime(course, day, locations, timetable_id, user_id):
    lecturer = Lecturer.objects.get(id=course.lecturer_id)
    department = Department.objects.get(id=course.department_id)
    lecturer_name = lecturer.other_names + " " + lecturer.surname
    department = Department.objects.get(id=course.department_id)
    college = College.objects.get(id=department.college_main_id)
    all_time = [i for i in range(1, college.rows_per_day+1)]
    for location in list(locations):
        if len(ExamSchedule.objects.filter(day=day, location_id=location)) > 0:
            check_List = list(dict(ExamSchedule.objects.filter(day=day, location_id=location).values_list("time", "id")))
            for time in list(all_time):
                if time in check_List: all_time.remove(time)
                else: pass
        for time in list(all_time):
            if time % 2 == 0: all_time.remove(time)
    rand_time = random.choice(all_time)
    for location in list(locations):
        location_name = Location.objects.get(id=location).name
        new_etable = ExamSchedule(
            course_id=course.id, course_name=course.name,
            location_id=location, location_name=location_name,
            lecturer_id=lecturer.id, lecturer_name=lecturer_name,
            time=rand_time, day=day, creator_id=user_id,
            timetable_id=timetable_id, department_id=department.id, 
            department_name=department.name, college_id=college.id, 
            college_name=college.name, course_code=course.code,
            size=course.estimated_class_size, year_group=course.year_group
        )
        new_etable.save()
        

