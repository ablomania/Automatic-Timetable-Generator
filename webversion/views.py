from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Lecturer, Location, Department, Course,Schedule
import json 
import random

# Create your views here.

#Homepage loader
def homePage(request):
    template = loader.get_template("index.html")
    context = {

    }
    return HttpResponse(template.render(context, request))


#Selection page loader
def secondPage(request, college, dname,id):
    template = loader.get_template("page2.html")
    department = Department.objects.get(name=dname, college=college)
    departments = Department.objects.filter(college=college)
    course = Course.objects.filter(department_id = department.id, year_group=id)
    average_Courses_Per_Day = 5

    if request.method == 'POST':
        b = dict(request.POST)
        b.pop("csrfmiddlewaretoken")
        print(b)
        createSchedule(dictionary=b, department=department, courses_per_day=average_Courses_Per_Day)
        


    lastdepartment = departments.filter().last().id
    firstdepartment = departments.filter().first().id
    page = id - 1
   
    if((page == 0) and (department.id != lastdepartment)):
        d = department.id + 1
        dname = departments.get(id = d)
        page = 4
    if((department.id == lastdepartment) and (page == 0)):
        pass

    context = {
        "course" : course, "departments" : departments,"college": college
        , "dname": dname, "page" : page, 
    }
    return HttpResponse(template.render(context, request))



#Timetable page loader
def timetable(request):
    template = loader.get_template("timetablepage.html")
    schedule = Schedule.objects.all().values()
    course = Course.objects.all().values()
    year1 = schedule.filter(year_group = 1)
    year2 = schedule.filter(year_group = 2)
    year3 = schedule.filter(year_group = 3)
    year4 = schedule.filter(year_group = 4)
    
    print(year2)
    context = {
        "schedule": schedule, "year1": year1, "year2": year2,
        "year3": year3, "year4": year4
    }
    return HttpResponse(template.render(context, request))



#function to create schedules
def createSchedule(dictionary, department, courses_per_day):
    for x in dictionary.values():
        current_course = Course.objects.get(id = x[0])
        hours = current_course.hours
        if(current_course.is_lab_only or current_course.has_labs):
            if(current_course.is_lab_only):
                createLab(course=x, department=department, height=current_course.lab_hours)
            if(current_course.has_labs):
                createLab(course=x, department=department, height=current_course.lab_hours)
                used_Locations = createClass(course=x, department=department, hours=hours, courses_per_day = courses_per_day)
        else:
            used_Locations = createClass(course=x, department=department, hours=hours, courses_per_day = courses_per_day)
        return used_Locations 

def createHours(hours):
    height = 0
    if(hours < 0):
        height = 1
    # if(hours == 0):
    #     height = 0
    if(hours >= 2):
        height = 2
    
    return height

def createClass(course, department, hours, courses_per_day):
    for y in range(hours):
        height =createHours(hours)
        if(hours == 0): break 
        hours = hours - 2     
        if(height > 0): 
            used_Locations = dict(Schedule.objects.values_list("row", "Location_id")) 
            current_course = Course.objects.get(id = course[0])
            max_row = 50
            
            is_Done = 0
            while is_Done <= 0:
                current_row = chooseRow(course = course, height = height, courses_per_day = courses_per_day)
                temp_data = dict()
                temp_location = createClassLocation(course = current_course.id, department = department)
                temp_data[current_row] = temp_location
                
                if(len(used_Locations) == 0):
                    class_location = temp_location
                    used_Locations[current_row] = class_location
                    is_Done = 1
                    break
                for x, y in list(used_Locations.items()):
                    if((x not in temp_data.keys()) and (y not in temp_data.values())):
                        is_Done = 1
                        class_location =temp_location
                        used_Locations[current_row] = class_location
                        break

            course_code = (Course.objects.get(id = course[0])).code
            lecturer = Lecturer.objects.get(id=((Course.objects.get(id = course[0])).lecturer_id))
            lecturer_name = lecturer.other_names + " " + lecturer.surname
            location_name = (Location.objects.get(id = class_location)).name
            print(lecturer_name)
            print(location_name)
            course_year_group = (Course.objects.get(id = course[0])).year_group        
            new_schedule = Schedule(lecturer_name = lecturer_name, location_name = location_name, course_code = course_code, year_group = course_year_group,course_id = course[0], department_id = department.id, height = height, column = department.id, Location_id = class_location, row = current_row)
            new_schedule.save()



def createClassLocation(course, department):
    current_course = Course.objects.get(id = course)
    current_course_size = current_course.estimated_class_size
    classroom = Location.objects.filter(is_Lab = False)
    locations = classroom.filter(capacity__gte = current_course_size)
    rand_Location = random.choice(locations.values())
    for x in rand_Location.values():
        rand_Location_id = x
        break
    current_Location = locations.get(id = rand_Location_id)
    print("create class location done")
    return current_Location.id


def chooseRow(course, height, courses_per_day):
    is_done = 0
    current_course = Course.objects.get(id = course[0])
    current_course_yg = current_course.year_group
    max_yg_row = 50 * current_course_yg
    min_yg_row = max_yg_row + 1 - 50
    # max_row = 2 * 5 * courses_per_day
    while is_done == 0:
        rand_row = random.randrange(min_yg_row, max_yg_row+1)
        if((rand_row==(courses_per_day*2)) or (rand_row==(courses_per_day*4)) or (rand_row==(courses_per_day*6)) or (rand_row==(courses_per_day*8)) or (rand_row==(courses_per_day*10))):
            if (height < 2):
                is_done = 1
                print("choose row 2nd if")
                break
            if(height > 2):
                rand_row = random.randrange(min_yg_row, max_yg_row+1)
                print("choose row else")
                is_done = 1
        else:
            break
        
    print("choose row ends")
    print(rand_row)
    return rand_row


def createLab(course, department, height):
        course_code = (Course.objects.get(id = course[0])).code
        course_year_group = (Course.objects.get(id = course[0])).year_group
        location = Location.objects.get(name = "LAB")
        new_schedule = Schedule(course_id = course[0], department_id = department.id, height = height, Location_id = location.id, column = department.id, course_code = course_code, year_group = course_year_group)
        new_schedule.save()



def createCourse(request):
    course = Course.objects.all().values()
    template = loader.get_template("createcourse.html")

    context = {}
    return HttpResponse(template.render(context, request))



def editCourse(request):
    template = loader.get_template("editcourse.html")
    course = Course.objects.all().values()

    context = {}
    return HttpResponse(template.render(context, request))