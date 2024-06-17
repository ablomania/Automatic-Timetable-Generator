from .models import Course, Lecturer, Schedule, Location, Department
import random, math

def createSchedule(course_id):
    current_course = Course.objects.get(id=course_id)
    current_department = Department.objects.get(id=current_course.department_id)
    column = chooseColumn(department=current_department)
    rows = chooseRow(course=current_course)
    row_size = len(rows)
    result = chooseLocation(course=current_course, rows=rows)
    for row, location in list(result.items()):
        location_name = Location.objects.get(id=location).name
        lecturer_name = Lecturer.objects.get(id=current_course.lecturer_id)
        new_schedule = Schedule(course_id=current_course.id, course_code=current_course.code, year_group=current_course.year_group,
                                location_id=location, location_name=location_name, height=2, column=column, row=row, department=current_department,
                                lecturer_name=lecturer_name, lecturer_id=current_course.lecturer_id)
        new_schedule.save()


def chooseRow(course,height = 2):
    is_combined = course.is_combined
    lect_id = course.lecturer_id
    credit_hours = int(course.hours)
    courses_per_day = 10
    number_of_schedules = credit_hours // 2
    remainder = credit_hours % 2
    year_group = course.year_group
    max_yg_row = year_group * 50
    min_yg_row = (max_yg_row + 1) - 50
    row = []
    used_rows = list(dict((Schedule.objects.filter(department_id=course.department_id, year_group=year_group).values_list("row", "id"))).values())
    number = 0
    while number <= number_of_schedules:
        factor = 0
        rand_row = random.randint(min_yg_row, max_yg_row)
        temp_rows = []
        pp = rand_row % 10
        if((rand_row-4 in used_rows) and (rand_row-2 in used_rows) and (course.has_labs is False)) or rand_row-1 in used_rows:
            continue
        if (lect_id in Schedule.objects.filter(department_id=course.department_id, year_group=year_group, row=rand_row)) or (lect_id in Schedule.objects.filter(department_id=course.department_id, year_group=year_group, row=rand_row+1)) and (is_combined==False):
            continue
        if((pp != 0) and (rand_row%2 != 0) and (rand_row < max_yg_row)):
            if row:
                m1 = math.floor((row[0]/10))
                m2 = math.floor((rand_row/10))
                if((m1 == m2) or (rand_row%10 == 0)):
                    continue
            for x in range(height):
                temp_rows.append((rand_row+factor))
                factor = factor + 1
            if(temp_rows not in used_rows):
                isDone = 0
                while isDone < 2:
                    row.append(temp_rows[isDone])
                    isDone = isDone + 1
                    number = number + 1
    while remainder != 0:
        rand_row = random.randrange(min_yg_row, max_yg_row)
        if(rand_row not in used_rows) and (rand_row not in row):
            remainder = remainder - 1
            row.append(rand_row)
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
    count = 1
    for row in rows:
        tt = dict(Schedule.objects.filter(row=row).values_list("id","row"))
        used = [x for x in tt.values()]
        if(course.has_labs or course.is_lab_only):
            print("has labs")
        
        if not course.has_labs:
            if(course.is_combined):
                location = Location.objects.get(capacity__gte = 500)
                res[row] = location.id
                return res
            isDone = 0
            while isDone == 0:
                classroom = Location.objects.filter(is_Lab=False, capacity__gte=current_course_size)
                if(count%2 == 1):
                    print("count is", count)
                    rand_location = random.choice(classroom.values())["id"]
                if(row in used):
                    ss = Schedule.objects.filter(row=row, location_id=rand_location)
                    if rand_location not in ss:
                        res[row]= rand_location
                        print("rand location not in")
                        count = count + 1
                        break 
                    if rand_location in ss:
                        print("rand location in")
                        continue
                    print("in")
                if(row not in used):
                    res[row] =rand_location
                    count = count + 1
                    print("free")
                    break
    return res


def createCourse(dictionary):
    code = dictionary['code'].upper()
    name = dictionary['name'].capitalize()
    lecturer = dictionary['lecturer']
    department = dictionary['department']
    hours = dictionary['hours']
    has_labs = dictionary['has_labs']
    is_combined = dictionary.get('is_combined', False)
    is_lab_only = dictionary.get('is_lab_only', False)
    lab_hours = dictionary.get('lab_hours', False)
    year_group = dictionary['year_group']
    estimated_class_size = dictionary['estimated_class_size']
    new_Course = Course(is_combined=is_combined, code=code, name=name, lecturer_id=lecturer, department_id=department, hours=hours, is_lab_only=is_lab_only, has_labs=has_labs, lab_hours=lab_hours, year_group=year_group, estimated_class_size=estimated_class_size)
    new_Course.save()

def modifyCourse(course, dictionary):
    currentCourse = course
    currentCourse.code = dictionary['code']
    currentCourse.name = dictionary['name']
    currentCourse.lecturer_id = dictionary['lecturer']
    currentCourse.department_id = dictionary['department']
    currentCourse.hours = dictionary['hours']
    currentCourse.has_labs = dictionary['has_labs']
    currentCourse.is_lab_only = dictionary['is_lab_only']
    currentCourse.lab_hours = dictionary['lab_hours']
    currentCourse.year_group = dictionary['year_group']
    currentCourse.estimated_class_size = dictionary['estimated_class_size']
    currentCourse.save()
