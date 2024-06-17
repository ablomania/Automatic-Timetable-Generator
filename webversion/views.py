from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Lecturer, Location, Department, Course,Schedule
from .functions import *
import random

# Create your views here.
global selected_courses
selected_courses = []
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
        for x in b.values():
            course_id = x[0]
            if course_id not in selected_courses:
                selected_courses.append(int(course_id))
        print(selected_courses)
    lastdepartment = departments.filter().last().id
    firstdepartment = departments.filter().first().id
    
    page = id - 1
    tp = id
    if((page == 0) and (department.id is not lastdepartment)):
        
        d = department.id + 1
        dname = departments.get(id = d)
        page = 4
    # if tp==0:
    #     return HttpResponseRedirect(reverse("viewSelected", args=(college, department.name)))
    if((department.id == lastdepartment) and (page == 0)):
        page = "viewselected"
    context = {
        "course" : course, "departments" : departments,"college": college
        , "dname": dname, "page" : page, "tp":tp, "department": department
    }
    return HttpResponse(template.render(context, request))


def viewSelected(request, college, dname):
    template = loader.get_template("vscourses.html")
    department = Department.objects.get(name=dname)
    courses = Course.objects.all()
    departments = Department.objects.filter(college=college)
    temp_list =[]
    for x in courses:
        if x.id in selected_courses:
            temp_list.append(x)
    print(temp_list)
    context = {
        "departments": departments, "list":temp_list, "college":college
    }
    return HttpResponse(template.render(context, request))


#Timetable page loader
def timetable(request, college):
    template = loader.get_template("timetablepage.html")
    schedule = Schedule.objects.order_by("row")
    course = Course.objects.all().values()
    departments = Department.objects.filter(college=college)
    ss =[]
    for course_id in selected_courses:
        createSchedule(course_id=course_id)
    some_list = list(range(1,1000))
    for sch in schedule:
        if sch.department in departments:
            ss.append(sch)
    scarr ={}
    nfds = len(departments) * 10
    row = list(" " * nfds)
    l1 = len(ss)
    for x in range(1, 21):
        scarr[x] = row
    temp = []
    tt =0
    for x in ss:
        group =(x.row // 10) + 1
        rem = x.row % 10
        position = round(((rem-1)*15) + (x.column-1))
        if x.row % 10 == 0:
            group = (x.row //10)
        temp = []
        temp = scarr[group].copy()
        hh=len(temp)
        print("position is ", position," and temp is", hh)
        temp[position] = x
        scarr[group] = temp
    times = ["PERIOD","8:00 - 8:55", "9:00 - 9:55", "10:30 - 11:25", "11:30 - 12:25", "1:00 - 1:55", "2:00 - 2:55", "3:00 - 3:55", "4:00 - 4:55", "5:00 - 5:55", "6:00 - 6:55"]
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    year_groups = [1, 2, 3, 4]
    context = {
        "schedule": schedule, "departments": departments, "scarr": scarr, "days": days,
        "year_groups":year_groups, "times":times
    }
    return HttpResponse(template.render(context, request))



#function to create schedules
# def createSchedule(dictionary, department, courses_per_day):
#     for x in dictionary.values():
#         current_row = chooseRow(course=x)
#         current_course = Course.objects.get(id = x[0])
#         hours = current_course.hours
#         if(current_course.is_lab_only or current_course.has_labs):
#             if(current_course.is_lab_only):
#                 createLab(course=x, department=department, height=current_course.lab_hours)
#             if(current_course.has_labs):
#                 createLab(course=x, department=department, height=current_course.lab_hours)
#                 used_Locations = createClass(course=x, department=department, hours=hours, courses_per_day = courses_per_day)
#         else:
#             used_Locations = createClass(course=x, department=department, hours=hours, courses_per_day = courses_per_day)
#         return used_Locations 

# def createHours(hours):
#     height = 0
#     if(hours < 0):
#         height = 1
#     # if(hours == 0):
#     #     height = 0
#     if(hours >= 2):
#         height = 2
    
#     return height

# def createClass(course, department, hours, courses_per_day):
#     department = (Course.objects.get(id = course[0])).department_id
#     for y in range(hours):
#         height =createHours(hours)
#         if(hours == 0): break 
#         hours = hours - 2     
#         if(height > 0): 
#             used_Locations = dict(Schedule.objects.values_list("row", "Location_id")) 
#             used_Lecturers = dict(Schedule.objects.values_list("row", "lecturer_id"))
#             current_course = Course.objects.get(id = course[0])
#             max_row = 50
            
#             is_Done = 0
#             while is_Done <= 0:
#                 current_row = chooseRow(course = course, height = height, courses_per_day = courses_per_day)
#                 temp_data = dict()
#                 currrent_Lecturer = (Course.objects.get(id =course[0])).lecturer_id
#                 temp_location = createClassLocation(course = current_course.id, department = department)
#                 temp_data[current_row] = temp_location
#                 temp_data["lecturer"] = currrent_Lecturer
                
#                 if(len(used_Locations) == 0 and len(used_Lecturers) == 0):
#                     class_location = temp_location
#                     used_Locations[current_row] = class_location
#                     is_Done = 1
#                     break
#                 for x, y in list(used_Locations.items()):
#                     if((x not in temp_data.keys()) and (y not in temp_data.values())):
#                         for w, z in list(used_Lecturers.items()):
#                             is_Done = 1
#                             class_location =temp_location
#                             used_Locations[current_row] = class_location
#                             break

#             course_code = (Course.objects.get(id = course[0])).code
#             lecturer = Lecturer.objects.get(id=((Course.objects.get(id = course[0])).lecturer_id))
#             lecturer_name = lecturer.other_names + " " + lecturer.surname
#             location_name = (Location.objects.get(id = class_location)).name
#             column = createColumn(department)
#             course_year_group = (Course.objects.get(id = course[0])).year_group        
#             new_schedule = Schedule(lecturer=lecturer,lecturer_name = lecturer_name, location_name = location_name, course_code = course_code, year_group = course_year_group,course_id = course[0], department_id = department, height = height, column = department, Location_id = class_location, row = current_row)
#             new_schedule.save()


# def createColumn(department):
#     current_college = (Department.objects.get(department=department)).college
#     department_group = (Department.objects.filter(college=current_college)).order_by("name")
#     column = 0
#     for x in department_group:
#         column = column + 1
#         if(x.id == department):
#             break
#     return column


# def createClassLocation(course, department):
#     current_course = Course.objects.get(id = course)
#     current_course_size = current_course.estimated_class_size
#     classroom = Location.objects.filter(is_Lab = False)
#     locations = classroom.filter(capacity__gte = current_course_size)
#     rand_Location = random.choice(locations.values())
#     for x in rand_Location.values():
#         rand_Location_id = x
#         break
#     current_Location = locations.get(id = rand_Location_id)
#     print("create class location done")
#     return current_Location.id


# def chooseRow(course, height, courses_per_day):
#     is_done = 0
#     current_course = Course.objects.get(id = course[0])
#     current_department = current_course.department_id
#     current_course_yg = current_course.year_group
#     max_yg_row = 50 * current_course_yg
#     min_yg_row = max_yg_row + 1 - 50
#     # max_row = 2 * 5 * courses_per_day
#     while is_done == 0:
#         aa = 5
#         while aa == 5:
#             rand_row = random.randrange(min_yg_row, max_yg_row+1)
#             if not Schedule.objects.filter(row = rand_row, department_id = current_department):
#                 aa = 9
#         if((rand_row==(courses_per_day*2)) or (rand_row==(courses_per_day*4)) or (rand_row==(courses_per_day*6)) or (rand_row==(courses_per_day*8)) or (rand_row==(courses_per_day*10))):
#             if (height < 2):
#                 is_done = 1
#                 print("choose row 2nd if")
#                 break
#             if(height > 2):
#                 rand_row = random.randrange(min_yg_row, max_yg_row+1)
#                 print("choose row else")
#                 is_done = 1
#         else:
#             break
        
#     print("choose row ends")
#     return rand_row


# def createLab(course, department, height):
#         department = (Course.objects.get(id = course[0])).department_id
#         course_code = (Course.objects.get(id = course[0])).code
#         course_year_group = (Course.objects.get(id = course[0])).year_group
#         location = Location.objects.get(name = "LAB")
#         current_row = chooseRow(course = course, height = height, courses_per_day = 5)
#         location_name = (Location.objects.get(id = location.id)).name
#         lecturer = Lecturer.objects.get(id=((Course.objects.get(id = course[0])).lecturer_id))
#         lecturer_name = lecturer.other_names + " " + lecturer.surname
#         new_schedule = Schedule(lecturer=lecturer,lecturer_name = lecturer_name, location_name = location_name, course_code = course_code, year_group = course_year_group,course_id = course[0], department_id = department, height = height, column = department, Location_id = location.id, row = current_row)
#         new_schedule.save()



def createCoursePage(request):
    course = Course.objects.all().values()
    template = loader.get_template("createcourse.html")
    slecturer = Lecturer.objects.all().values()
    departments = Department.objects.all().values()

    if request.method == "POST":
        createCourse(request.POST)

    context = {
        "lecturer": slecturer, "departments": departments
    }
    return HttpResponse(template.render(context, request))




def optionsPage(request):
    template = loader.get_template("optionsPage")
    if request.method == "POST":
        dictionary = request.POST
        collegename = dictionary['college'].upper()
        departmentCount = int(dictionary['depmntCount'])
        count = list(range(1,departmentCount+1))
    context = {
        "collegename": collegename, "count": count,
    }
    return HttpResponse(template.render(context, request))

def viewDepartments(request, collegename):
    template = loader.get_template("depts.html")
    if request.method =="POST":
        bb =dict(request.POST)
        bb.pop('csrfmiddlewaretoken')
        d = "department"
        d1 = 0
        nums = 1
        m = "max_yg"
        m1 =0
        for x, y in list(bb.items()):
            dd = d + str(nums)
            mm = m + str(nums)
            if(x == dd):
                department = y[0].upper()
                d1 = d1 + 1
                continue
            if(x == mm):
                max_yg = y[0]
                m1 = m1 + 1
            if(d1==m1):
                if not Department.objects.filter(name=department,college=collegename):
                    new_Department = Department(name=department, college=collegename, max_yg=max_yg)
                    new_Department.save()
            nums = nums + 1
    
    departments = Department.objects.filter(college=collegename)
    first_department = departments.filter().first()
    first_department_name = departments.filter().first().name
    
    context = {
        "departments": departments, "collegename" : collegename, "first": first_department_name,
        "max_yg" : first_department.max_yg
    }
    return HttpResponse(template.render(context, request))



def editCourse(request, code):
    template = loader.get_template("editcourse.html")
    course = Course.objects.get(code=code)
    slecturer = Lecturer.objects.all().values()
    cdepartment = Department.objects.get(id=course.department_id)
    clecturer = Lecturer.objects.get(id=course.lecturer_id)
    departments = Department.objects.all().values()
    bool_List = [True, False]
    if request.method == "POST":
        dictionary = request.POST
        modifyCourse(course=course, dictionary=dictionary)
        return HttpResponseRedirect(reverse('pagetwo',args=(cdepartment.college, cdepartment.name, course.year_group)))

    context = {"course": course, "lecturer":slecturer, "departments": departments,
               "clecturer": clecturer, "cdepartment": cdepartment, "bool_List": bool_List
               }
    return HttpResponse(template.render(context, request))

def createDepartment(request):
    template = loader.get_template("createdept.html")
    if request.method == "POST":
        dictionary = request.POST
        name = dictionary['name'].upper()
        college = dictionary['college'].upper()
        new_Department = Department(name=name, college=college)
        new_Department.save()

    context = {}
    return HttpResponse(template.render(context, request))


def createLecturer(request):
    template = loader.get_template("createlecturer.html")
    departments = Department.objects.all().values()
    if request.method == "POST":
        dictionary = request.POST
        surname = dictionary['surname'].capitalize()
        other_names = dictionary['other_names'].capitalize()
        department = dictionary['department']
        new_Lecturer = Lecturer(surname=surname, other_names=other_names, department_id=department)
        new_Lecturer.save()

    context = {
        "departments": departments,
    }
    return HttpResponse(template.render(context, request))