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
    max_yg = department.max_yg
    year_groups = [i for i in range(1,max_yg+1)]
    course = Course.objects.filter(department_id = department.id, year_group=id)
    average_Courses_Per_Day = 5
    if request.method == 'POST':
        b = dict(request.POST)
        b.pop("csrfmiddlewaretoken")
        for x in b.values():
            course_id = int(x[0])
            current_course = Course.objects.get(id=course_id)
            if (current_course.has_labs or current_course.is_lab_only):
                selected_courses.insert(0, int(course_id))
            if(course_id not in selected_courses):
                selected_courses.append(int(course_id))
            if 'save' in request.POST:
                HttpResponseRedirect(reverse('pagetwo',args=(college, dname, tp)))
            
           
        print(selected_courses)
    result = {}
    for course_id in selected_courses:
        scourse = Course.objects.get(id=course_id)
        result[course_id] = scourse

    if request.method == "GET" and 'btnsidebar_remove' in request.GET:
        remove_dict = dict(request.GET)
        remove_dict.pop('csrfmiddlewaretoken')
        remover = int(remove_dict["btnsidebar_remove"][0])
        print("remove dict is ", remove_dict)
        print(remover)
        if remover in selected_courses:
            selected_courses.remove(remover)
        return HttpResponseRedirect(reverse('pagetwo',args=(college, dname, id)))
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
        "courses" : course, "departments" : departments,"college": college
        ,"ldept":lastdepartment, "result":result, "year_groups": year_groups, "dname": dname, "page" : page, "tp":tp, "department": department
    }
    return HttpResponse(template.render(context, request))


def viewSelected(request, college):
    template = loader.get_template("vscourses.html")
    courses = Course.objects.all()
    departments = Department.objects.filter(college=college)
    year_groups = [i for i in range(1,20+1)]
    temp_list =[]
    for x in courses:
        if x.id in selected_courses:
            temp_list.append(x)
    print(temp_list)
    context = {
        "y_gs": year_groups, "departments": departments, "list":temp_list, "college":college
    }
    return HttpResponse(template.render(context, request))


#Timetable page loader
def timetable(request, college):
    template = loader.get_template("timetablepage.html")
    schedule = Schedule.objects.order_by("row")
    course = Course.objects.all().values()
    departments = Department.objects.filter(college=college)
    # For the buttons
    if request.method == "POST":
        if 'regenerate' in request.POST or 'generate' in request.POST:
            Schedule.objects.all().delete()
            for course_id in selected_courses:
                createSchedule(course_id=course_id)
            return HttpResponseRedirect(reverse("timetablePage", args=(college)))
        if 'save' in request.POST:
            pass
    ss =[]
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
        temp[position] = x
        scarr[group] = temp
    times = ["PERIOD","8:00 - 8:55", "9:00 - 9:55", "10:30 - 11:25", "11:30 - 12:25", "1:00 - 1:55", "2:00 - 2:55", "3:00 - 3:55", "4:00 - 4:55", "5:00 - 5:55", "6:00 - 6:55"]
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    year_groups = [1, 2, 3, 4]
    context = {
        "schedule": schedule, "departments": departments, "scarr": scarr, "days": days,
        "year_groups":year_groups, "times":times, "college":college
    }
    return HttpResponse(template.render(context, request))


def createCoursePage(request, department_id, year_group):
    course = Course.objects.all().values()
    template = loader.get_template("createcourse.html")
    department = Department.objects.get(id=department_id)
    college = Department.objects.get(id=department_id).college
    slecturer = Lecturer.objects.all().order_by("surname")
    departments = Department.objects.all().filter(college=college).order_by("name")

    if request.method == "POST":
        createCourse(request.POST)
    context = {
        "lecturer": slecturer, "departments": departments, "department":department,
        "year_group": year_group
    }
    return HttpResponse(template.render(context, request))

def deleteCourse(request, college, dname, year_group):
    if request.method =='POST':
        dictionary = dict(request.POST)
        dictionary.pop("csrfmiddlewaretoken")
        for x in dictionary.values():
            course_id = int(x[0])
            Course.objects.all().get(id=course_id).delete()
        return HttpResponseRedirect(reverse("pagetwo", args=(college,dname,year_group)))


def optionsPage(request):
    template = loader.get_template("optionsPage.html")
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


def allLecturers(request):
    template = loader.get_template("alllecturers.html")
    departments = Department.objects.all()
    lecturers = Lecturer.objects.all().order_by("other_names")
    context = {
        "lecturers":lecturers, "departments":departments,
    }
    return HttpResponse(template.render(context, request))

def deleteLecturer(request, id):
    if request.method == "POST":
        current_lecturer = Lecturer.objects.get(id=id)
        current_lecturer.delete()
        return HttpResponseRedirect(reverse("alllecturers"))

def createLecturer(request):
    template = loader.get_template("createlecturer.html")
    departments = Department.objects.all().values()
    if request.method == "POST":
        dictionary = request.POST
        surname = dictionary['surname'].capitalize()
        other_names = dictionary['other_names'].upper()
        department = dictionary['department']
        new_Lecturer = Lecturer(surname=surname, other_names=other_names, department_id=department)
        new_Lecturer.save()
    context = {
        "departments": departments,
    }
    return HttpResponse(template.render(context, request))

def modifyLecturerPage(request, lecturer_id):
    currentlect = Lecturer.objects.get(id=lecturer_id)
    department = Department.objects.get(id=currentlect.department_id)
    departments = Department.objects.all()
    template = loader.get_template("modifylect.html")
    if request.method == "POST":
        dictionary = request.POST
        modifylecturer(lecturer_id=lecturer_id, dictionary=dictionary)
        return HttpResponseRedirect(reverse('alllecturers'))
    context = {
        "currentlect":currentlect, "departments":departments, "department":department
    }
    return HttpResponse(template.render(context, request))

def locations(request):
    template = loader.get_template("all-locations.html")
    locations = Location.objects.all().order_by("name")
    departments = Department.objects.all().order_by("name")
    context = {
        "locations":locations, "departments":departments
    }
    return HttpResponse(template.render(context, request))

def deleteLocation(request, id):
    if request.method == "POST":
        current_location = Location.objects.get(id=id)
        current_location.delete()
        return HttpResponseRedirect(reverse("locations"))


def addalocation(request):
    if request.method == "POST":
        dictionary = request.POST
        name = dictionary['name'].upper()
        capacity = int(dictionary['capacity'])
        about = dictionary['about'].capitalize()
        is_in_same_college = dictionary.get('is_in_same_college', False)
        college = dictionary['college'].upper()
        new_location = Location(
            college=college, name=name, capacity=capacity, about=about, is_in_same_college=is_in_same_college
        )
        new_location.save()
    return HttpResponseRedirect(reverse('locations'))

def modifylocation(request, id):
    template = loader.get_template("edit-location.html")
    location = Location.objects.get(id=id)
    boolist = [True, False]
    if request.method == "POST":
        dictionary = request.POST
        currentlocation = Location.objects.get(id=id)
        currentlocation.name = dictionary['name'].upper()
        currentlocation.capacity = int(dictionary['capacity'])
        currentlocation.about = dictionary['about']
        currentlocation.is_in_same_college = dictionary.get('is_in_same_college', False)
        currentlocation.save()
        return HttpResponseRedirect(reverse("locations"))
    context = {
        'location':location, "boolist":boolist
    }
    return HttpResponse(template.render(context, request))


def deleteDepartment(request, id):
    if request.method == "POST":
        current_department = Department.objects.get(id=id)
        current_department.delete()
        return HttpResponseRedirect(reverse("alllecturers"))