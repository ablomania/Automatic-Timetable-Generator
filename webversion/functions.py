from .models import Course, College, UserAccount, Lecturer, Schedule, Location, Department, Pref_Stuff
import random, math
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import docx

def createSchedule(course_id, user_id, timetable):
    if len(Course.objects.filter(id=course_id)) > 0:
        current_course = Course.objects.get(id=course_id)
        current_department = Department.objects.get(id=current_course.department_id)
        college_id = current_department.college_main_id
        college = College.objects.get(id=current_department.college_main_id)
        rows_per_day = college.rows_per_day
        days_per_week = college.days_per_week
        year_group = current_course.year_group
        max_yg_row = year_group * (rows_per_day * days_per_week)
        min_yg_row = (max_yg_row + 1) - (rows_per_day * days_per_week)
        #create lab sessions for courses with labs
        if current_course.has_labs or current_course.is_lab_only:
            createLab(course=current_course, user_id=user_id, college_id=college_id, timetable_id=timetable)
            if current_course.is_lab_only:
                return
        preferred = Pref_Stuff.objects.filter(course_id=course_id)
        if preferred:
            createPreferred(course_id=course_id, user_id=user_id, timetable_id=timetable)
        else:
            column = chooseColumn(department=current_department)
            locations = chooseLocation(course=current_course, user_id=user_id)
            result = chooseRow(course=current_course, locations=locations, is_lab=False, user_id=user_id, timetable=timetable)
            for row, location in list(result.items()):
                location_name = Location.objects.get(id=location).name
                lecturer_name = Lecturer.objects.get(id=current_course.lecturer_id)
                if row % 10 == 0:
                    time = rows_per_day
                    day = int((row - min_yg_row + 1) / rows_per_day)
                else:
                    time = (row - min_yg_row + 1) % rows_per_day
                    day = int((row - min_yg_row + 1) / rows_per_day) + 1
                new_schedule = Schedule(course_id=current_course.id, course_code=current_course.code, year_group=current_course.year_group,
                                        location_id=location, location_name=location_name, height=2, column=column, row=row, department=current_department,
                                        lecturer_name=lecturer_name, lecturer_id=current_course.lecturer_id, creator_id=user_id, time=time, day=day,
                                        college_id=college_id, college_name=college.name, timetable_id=timetable
                                )
                new_schedule.save()

def createPreferred(course_id, user_id, timetable):
    print("preferred started")
    preferred = Pref_Stuff.objects.filter(course_id=course_id)
    course = Course.objects.get(id=course_id)
    department = Department.objects.get(id=course.department_id)
    college = College.objects.get(id=department.college_main_id)
    year_group = course.year_group
    rows_per_day = college.rows_per_day
    lecturer = Lecturer.objects.get(id=course.lecturer_id)
    lecturer_name = lecturer.other_names + " " + lecturer.surname
    days_per_week = college.days_per_week
    max_yg_row = year_group * (rows_per_day * days_per_week)
    min_yg_row = (max_yg_row + 1) - (rows_per_day * days_per_week)
    hours = course.hours
    column = chooseColumn(department=department)
    print("preferred length is : ", len(preferred))
    for pf in list(preferred):
        hours = hours - 2
        pf_loc = pf.location
        if hours >= 0: height = 2
        else: height = 1
        row = ((pf.day - 1)*college.rows_per_day) + pf.time + (min_yg_row-1)
        for h in range(height):
            new_schedule = Schedule(
                course_id=course_id, course_code=course.code,
                year_group=year_group, location_id=pf.location_id,
                location_name=pf_loc.name, height=height,
                column=column, row=row, department_id=department.id,
                lecturer_name=lecturer_name, lecturer_id=lecturer.id,
                creator_id=user_id, college_id=college.id,
                day=pf.day, time=pf.time, college_name=college.name,
                timetable_id=timetable,
            )
            new_schedule.save()
            row = row + 1
            if hours < 0: break
    print("preferred ended")


def createLab(course, user_id, college_id, timetable):
    print("create lab started")
    column = chooseColumn(department=course.department)
    lab = Location.objects.get(name="LAB").id
    rows = chooseRow(course=course, locations=lab, is_lab=True, user_id=user_id, timetable=timetable)
    lecturer = Lecturer.objects.get(id=course.lecturer_id)
    college = College.objects.get(id=Department.objects.get(id=course.department_id).college_main_id)
    rows_per_day = college.rows_per_day
    days_per_week = college.days_per_week
    lecturer_name = lecturer.other_names + " " + lecturer.surname
    year_group = course.year_group
    max_yg_row = year_group * (rows_per_day * days_per_week)
    min_yg_row = (max_yg_row + 1) - (rows_per_day * days_per_week)
    for row in list(rows):
        if row % 10 == 0:
            time = rows_per_day
            day = int((row - min_yg_row + 1) / rows_per_day)
        else:
            time = (row - min_yg_row + 1) % rows_per_day
            day = int((row - min_yg_row + 1) / rows_per_day) + 1
        new_lab = Schedule(
            course_id=course.id, course_code=course.code, year_group=course.year_group,
            location_id=lab, location_name="LAB", height=0, column=column,row=row,
            department_id=course.department_id, lecturer_name=lecturer_name, lecturer_id=course.lecturer_id,
            creator_id=user_id, college_id=college_id, time=time, day=day, college_name=college.name,
            timetable_id=timetable
        )
        new_lab.save()
    print("create lab ended")

def lister(mylist, min_yg_row):
    for element in list(mylist):
        new_element = element - min_yg_row + 1
        mylist.insert(0, int(new_element))
        mylist.remove(element)
    return mylist

def chooseRow(course, is_lab, locations, user_id, timetable, height = 2):
    print("choose row started")
    lect_id = course.lecturer_id
    print(course.name)
    print("lab = ", is_lab)
    credit_hours = int(course.hours)
    if is_lab: credit_hours = int(course.lab_hours)
    college = College.objects.get(id=Department.objects.get(id=course.department_id).college_main_id)
    rows_per_day = college.rows_per_day
    days_per_week = college.days_per_week
    number_of_schedules = credit_hours//2
    remainder = credit_hours % 2
    year_group = course.year_group
    max_yg_row = year_group * (rows_per_day * days_per_week)
    min_yg_row = (max_yg_row + 1) - (rows_per_day * days_per_week)
    rows = used_rows =  busylect = []
    result = {}
    odd_rows = []
    print("1")
    used_rows_list = list(dict(Schedule.objects.filter(department_id=course.department_id, year_group=year_group, row__gte=(min_yg_row), creator_id=user_id, timetable_id=timetable).values_list("row", "id")))
    used_rows = lister(mylist=used_rows_list, min_yg_row=min_yg_row)
    all_rows =[i for i in range(1,51)]
    lecturer_id = course.lecturer_id
    busylect_list = list(dict(Schedule.objects.filter(lecturer_id=lecturer_id, creator_id=user_id, timetable_id=timetable).values_list("row", "id"))) 
    busylect = lister(mylist=busylect_list, min_yg_row=min_yg_row)
    if not is_lab:
        print("2")
        print(all_rows)
        for location, h in list(locations.items()):
            banned_rows = list(dict(Schedule.objects.filter(location_id=location, timetable_id=timetable).values_list("row", "id")))
            for p in list(all_rows):
                for u in list(used_rows):
                    if int(p) == int(u): 
                        all_rows.remove(p)
                    else: pass
            print(all_rows)
            for p in list(all_rows):
                for b in list(banned_rows):
                    if int(p) == int(b): 
                        all_rows.remove(p)
                    else: pass
            # for p in list(all_rows):
            #     for c in list(combined_columns):
            #         if int(p) == int(c): 
            #             all_rows.remove(p)
            for p in list(all_rows):
                for b in list(busylect):
                    if int(p) == int(b):  
                        all_rows.remove(p)
                    else: pass
            for p in list(all_rows):
                if int(p) % 2 == 1: odd_rows.append(p)
                else: pass
            isDone = 0
            ss = 0
            print("3")
            while isDone == 0:
                rand_row = random.choice(odd_rows)
                # rand_row = rand_row + 2
                print("rand row is ", rand_row)
                if rand_row in all_rows:
                    second_row = rand_row+1
                    print("rand row in all rows")
                    if second_row in all_rows:
                        print("second row in all rows")
                        isDone = 1
                        break
                    else: pass
                else: pass
            print(rand_row)
            rows.append(rand_row+min_yg_row-1)
            result[rand_row+min_yg_row-1] =location
            if h == 2: 
                rows.append(second_row+min_yg_row-1)
                result[second_row+min_yg_row-1]=location
            print(rows)
            print("4")
            test1 = int(rand_row/10)
            for x in list(all_rows):
                test2 = int(x/10)
                if test1 == test2:
                    all_rows.remove(x)
        return result
    else:
        row = []
        number = 0
        while len(row) < (2*number_of_schedules):
            print("loop :", number)
            if((course.is_contiguous_lab_time) and (course.lab_hours >0)):
                rand_row = random.choice([i*10+1 for i in range(int(min_yg_row/10),int(max_yg_row/10))])
                row_range = [i for i in range(rand_row, rand_row+credit_hours)]
                skip = False
                print("is conti")
                for x in list(row_range):
                    for y in list(used_rows):
                        if int(x) == int(y):
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
                    unavailable_lect = list(dict(Schedule.objects.filter(department_id=course.department_id, year_group=year_group, row=test_row, creator_id=user_id, timetable_id=timetable).values_list("lecturer_id", "id")))
                    # print(unavailable_lect)
                    if ((lect_id in unavailable_lect)):
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
    print("choose row ended")
        

def chooseColumn(department):
    current_college_id = (Department.objects.get(id=department.id)).college_main_id
    department_group = list(dict((Department.objects.filter(college_main_id=current_college_id)).values_list("name", "id")))
    current_department = (Department.objects.get(id=department.id)).name
    column = 1
    department_group.sort()
    for x in department_group:
        if current_department in x:
            return column
        column = column + 1
    return -1

def chooseLocation(course, user_id):
    class_size = int(course.estimated_class_size)
    number_of_schedules = int(math.ceil(course.hours / 2))
    locations = list(dict(Location.objects.filter(capacity__gte=class_size, is_Lab=False, creator_id=user_id).values_list("id", "name")))
    department = Department.objects.get(id=course.department_id)
    college = department.college
    college_main_id = department.college_main_id
    departments = Department.objects.filter(creator_id=user_id)
    preferred = Pref_Stuff.objects.filter(college_main_id=college_main_id, creator_id=user_id, course_id=course.id)
    is_local = departments.filter(code=course.code)
    if is_local: locations = list(dict(Location.objects.filter(college__icontains=college, capacity__gte=class_size, is_Lab=False, creator_id=user_id).values_list("id", "name")))
    locations_list = {}
    height_list = []
    hours = course.hours
    count = 0
    # temp_locations = list(dict(Schedule.objects.filter(creator_id=user_id, course_code__icontains=course.code, lecturer_id=course.lecturer_id, college_id=department.college_main_id, batch=batch).values_list("location_id", "id")))
    for number in range(number_of_schedules):
        hours = hours -2
        if hours >= 0: height = 2
        else: height = 1
        rand_location = random.choice(locations)
        locations_list[rand_location]=height
        # else:
        #     for pref in preferred: preferred_locations.append(pref.location_id)
        #     current_pref = preferred_locations[count]
        #     locations_list[current_pref] = height
        #     count = count + 1
    print("location list is : ",locations_list)
    return locations_list

def createCourse(dictionary, user_id):
    code = dictionary['code'].upper()
    name = dictionary['name'].upper()
    lecturer = dictionary['lecturer']
    department = dictionary['department']
    hours = dictionary['hours']
    has_labs = dictionary.get('has_labs', False)
    is_lab_only = dictionary.get('is_lab_only', False)
    is_contiguous_lab_time = dictionary.get('is_contiguous_lab_time', False)
    lab_hours = dictionary.get('lab_hours', False)
    year_group = dictionary['year_group']
    estimated_class_size = dictionary['estimated_class_size']
    # preferred_location = dictionary[]
    new_Course = Course(
        creator_id=user_id, is_contiguous_lab_time=is_contiguous_lab_time,
          code=code, name=name, lecturer_id=lecturer, department_id=department,
            hours=hours, is_lab_only=is_lab_only, has_labs=has_labs, lab_hours=lab_hours,
              year_group=year_group, estimated_class_size=estimated_class_size,
              )
    new_Course.save()
    return new_Course



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
    return currentCourse


def modifylecturer(lecturer_id, dictionary):
    currentlect = Lecturer.objects.get(id=lecturer_id)
    currentlect.surname = dictionary['surname']
    currentlect.other_names = dictionary['other_names']
    currentlect.department_id = dictionary['department']
    currentlect.telephone = dictionary['telephone']
    currentlect.email = dictionary['email']
    currentlect.save()


        
