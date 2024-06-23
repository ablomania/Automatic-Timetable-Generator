from .models import Course, Lecturer, Schedule, Location, Department
import random, math
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def createSchedule(course_id):
    current_course = Course.objects.get(id=course_id)
    current_department = Department.objects.get(id=current_course.department_id)
    #create lab sessions for courses with labs
    if current_course.has_labs or current_course.is_lab_only:
        createLab(course=current_course)
        if current_course.is_lab_only:
            return
    column = chooseColumn(department=current_department)
    rows = chooseRow(course=current_course, is_lab=False)
    row_size = len(rows)
    result = chooseLocation(course=current_course, rows=rows)
    for row, location in list(result.items()):
        location_name = Location.objects.get(id=location).name
        lecturer_name = Lecturer.objects.get(id=current_course.lecturer_id)
        new_schedule = Schedule(course_id=current_course.id, course_code=current_course.code, year_group=current_course.year_group,
                                location_id=location, location_name=location_name, height=2, column=column, row=row, department=current_department,
                                lecturer_name=lecturer_name, lecturer_id=current_course.lecturer_id)
        new_schedule.save()

def createLab(course):
    rows = chooseRow(course=course, is_lab=True)
    column = chooseColumn(department=course.department)
    lab = Location.objects.get(name="LAB").id
    lecturer = Lecturer.objects.get(id=course.lecturer_id)
    lecturer_name = lecturer.other_names + " " + lecturer.surname
    for row in rows:
        new_lab = Schedule(
            course_id=course.id, course_code=course.code, year_group=course.year_group,
            location_id=lab, location_name="LAB", height=0, column=column,row=row,
            department_id=course.department_id, lecturer_name=lecturer_name, lecturer_id=course.lecturer_id
        )
        new_lab.save()


def chooseRow(course, is_lab, height = 2):
    is_combined = course.is_combined
    lect_id = course.lecturer_id
    credit_hours = int(course.hours)
    if is_lab: credit_hours = int(course.lab_hours)
    courses_per_day = 10
    number_of_schedules = credit_hours // 2
    remainder = credit_hours % 2
    year_group = course.year_group
    max_yg_row = year_group * 50
    min_yg_row = (max_yg_row + 1) - 50
    row = []
    used_rows = list(dict((Schedule.objects.filter(department_id=course.department_id, year_group=year_group).values_list("row", "id"))).values())
    number = 0
    while len(row) < (2*number_of_schedules):
        print("loop :", number)
        if((course.is_contiguous_lab_time) and (course.lab_hours >0)):
            rand_row = random.choice([i*10+1 for i in range(int(min_yg_row/10),int(max_yg_row/10))])
            row_range = [i for i in range(rand_row, rand_row+credit_hours)]
            skip = False
            print("is conti")
            for x in row_range:
                if x in used_rows:
                    skip = True
                    print("In used rows : skip")
                else: return row_range
            if skip: 
                print("skipping")
                continue
        else:
            factor = 0
            rand_row = random.randint(min_yg_row, max_yg_row)
            temp_rows = []
            test_row = rand_row
            pp = rand_row % 10
            if((rand_row-4 in used_rows) and (rand_row-2 in used_rows) and (course.has_labs is False) or (rand_row-1 in used_rows)):
                print("occupied: ")
                continue
            test_num = 0
            for count in range(height):
                unavailable_lect = list(dict(Schedule.objects.filter(department_id=course.department_id, year_group=year_group, row=test_row).values_list("lecturer_id", "id")))
                # print(unavailable_lect)
                if ((lect_id in unavailable_lect) and (is_combined==False)):
                    test_num == 1
                test_row = test_row + 1
            if(test_num == 1):
                print("i am working")
                continue
            if((pp != 0) and (rand_row%2 != 0) and (rand_row < max_yg_row)):
                print("pp not sati ")
                if row:
                    m1 = math.floor((row[0]/10))
                    m2 = math.floor((rand_row/10))
                    if((m1 == m2) or (rand_row%10 == 0)):
                        continue
                for x in range(height):
                    temp_rows.append((rand_row+factor))
                    factor = factor + 1
                if((temp_rows not in used_rows) and (temp_rows not in row)):
                    isDone = 0
                    while isDone < 2:
                        row.append(temp_rows[isDone])
                        print(row)
                        isDone = isDone + 1
                        number = number + 1
    while remainder != 0:
        rand_row = random.randrange(min_yg_row, max_yg_row)
        lrow =row[-1] + 1
        if is_lab and (lrow not in used_rows):
            row.append(lrow)
        if(rand_row not in used_rows) and (rand_row not in row):
            remainder = remainder - 1
            row.append(rand_row)
    print("course name: ", course.name)
    print("row is ", row)
    return row
    

def chooseColumn(department):
    current_college = (Department.objects.get(id=department.id)).college
    department_group = list(dict((Department.objects.filter(college=current_college)).values_list("name", "id")))
    current_department = (Department.objects.get(id=department.id)).name
    column = 1
    department_group.sort()
    for x in department_group:
        if current_department in x:
            return column
        column = column + 1
    return -1

def chooseLocation(course, rows):
    current_course_size = course.estimated_class_size
    res = {}
    saved_row = 0
    saved_location = 0
    for row in rows:
        used_loc_for_row = list(dict(Schedule.objects.filter(row=row).values_list("location_id","row")))
        if row+1 in rows:
            used_loc_for_row2 = list(dict(Schedule.objects.filter(row=(row+1)).values_list("location_id","row")))
        if not course.is_lab_only:
            if((row-1 != saved_row) and (row != 1)):
                classrooms = list(dict(Location.objects.filter(is_Lab=False, capacity__gte=current_course_size).values_list("id", "name")))
                for classroom in list(classrooms):
                    if((classroom in used_loc_for_row) or (classroom in used_loc_for_row2)):
                        classrooms.remove(classroom)
                rand_classroom = random.choice(classrooms)   
            saved_row = row
            saved_location = rand_classroom
            res[saved_row] = saved_location    
    return res


def createCourse(dictionary):
    code = dictionary['code'].upper()
    name = dictionary['name'].upper()
    lecturer = dictionary['lecturer']
    department = dictionary['department']
    hours = dictionary['hours']
    has_labs = dictionary.get('has_labs', False)
    is_combined = dictionary.get('is_combined', False)
    is_lab_only = dictionary.get('is_lab_only', False)
    is_contiguous_lab_time = dictionary.get('is_contiguous_lab_time', False)
    lab_hours = dictionary.get('lab_hours', False)
    year_group = dictionary['year_group']
    estimated_class_size = dictionary['estimated_class_size']
    new_Course = Course(is_contiguous_lab_time=is_contiguous_lab_time, is_combined=is_combined, code=code, name=name, lecturer_id=lecturer, department_id=department, hours=hours, is_lab_only=is_lab_only, has_labs=has_labs, lab_hours=lab_hours, year_group=year_group, estimated_class_size=estimated_class_size)
    new_Course.save()


def modifyCourse(course, dictionary):
    currentCourse = course
    currentCourse.code = dictionary['code'].upper()
    currentCourse.name = dictionary['name'].upper()
    currentCourse.lecturer_id = dictionary['lecturer']
    currentCourse.department_id = dictionary['department']
    currentCourse.hours = dictionary['hours']
    currentCourse.has_labs = dictionary['has_labs']
    currentCourse.is_lab_only = dictionary['is_lab_only']
    currentCourse.is_contiguous_lab_time = dictionary.get('is_contiguous_lab_time', False)
    currentCourse.lab_hours = dictionary['lab_hours']
    currentCourse.year_group = dictionary['year_group']
    currentCourse.estimated_class_size = dictionary['estimated_class_size']
    currentCourse.save()


def modifylecturer(lecturer_id, dictionary):
    currentlect = Lecturer.objects.get(id=lecturer_id)
    currentlect.surname = dictionary['surname']
    currentlect.other_names = dictionary['other_names']
    currentlect.department_id = dictionary['department']
    currentlect.save()