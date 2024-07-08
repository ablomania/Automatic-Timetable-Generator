from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import UserAccount, College, Lecturer, Location, Department, Course,Schedule
from .functions import *
import random

# Create your views here.
global selected_courses
selected_courses = []
#Homepage loader
def homePage(request):
    template = loader.get_template("index.html")
    emails = list(dict(UserAccount.objects.values_list("email", "password")))
    if request.method == "POST":
        dictionary = request.POST
        userEmail = dictionary['email'].lower()
        if userEmail in emails:
            return HttpResponseRedirect(reverse("colleges", args=(userEmail,)))
        else:
            return HttpResponseRedirect("errorInputPage")
    context = {

    }
    return HttpResponse(template.render(context, request))


def createAccountPage(request):
    template = loader.get_template("create-account.html")
    if request.method == "POST":
        dictionary = request.POST
        new_email = dictionary['email']
        new_user = UserAccount(email=new_email)
        new_user.save()
        return HttpResponseRedirect(reverse("colleges", args=(new_email,)))
    context = {}
    return HttpResponse(template.render(context, request))

def errorInputPage(request):
    template = loader.get_template("error-input.html")
    context = {}
    return HttpResponse(template.render(context, request))

def collegePage(request, email):
    user_id = UserAccount.objects.get(email=email).id
    departments = Department.objects.filter(creator_id=user_id,  )
    template = loader.get_template("colleges.html")
    user = UserAccount.objects.get(email=email)
    colleges = College.objects.filter(creater_id = user.id)
    context = {
        "colleges": colleges, "email": email,
    }
    return HttpResponse(template.render(context, request))

def collegeviewGenerator(request, email, college_id):
    if request.method == "GET":
        college = College.objects.get(id=college_id)
        department = Department.objects.filter(college_main_id=college.id).order_by("name").first()
        if department:
            max_yg = department.max_yg
            return HttpResponseRedirect(reverse("pagetwo", args=(email, college.id, department.name, max_yg)))
        else: return HttpResponseRedirect(reverse("createDept", args=(email, college_id)))

def createCollege(request, email):
    user_id = UserAccount.objects.get(email=email).id
    if request.method == "POST":
        dictionary = request.POST
        count = int(dictionary['count'])
        name = dictionary['name'].upper()
        days_per_week = int(dictionary['days'])
        rows_per_day = int(dictionary['rows'])
        new_college = College(
            name=name, creater_id=user_id, days_per_week=days_per_week, rows_per_day=rows_per_day
            )
        new_college.save()
        return HttpResponseRedirect(reverse("toBegin", args=(email, new_college.id, count)))

def editcollege(request, email, college_id):
    user_id = UserAccount.objects.get(email=email)
    template = loader.get_template("edit-college.html")
    college = College.objects.get(id=college_id)
    departments = Department.objects.filter(college_main_id=college_id)
    if request.method == "POST":
        dictionary = request.POST
        college.name = dictionary['name']
        college.rows_per_day = dictionary['rows']
        college.days_per_week = dictionary['days']
        college.save()
        return HttpResponseRedirect(reverse("colleges", args=(email,)))
    context = {
        "college":college, "departments":departments, "email":email,
    }
    return HttpResponse(template.render(context, request))

def deletecollege(request, email, id):
    if request.method == "POST":
        college = College.objects.get(id=id)
        college.delete()
        return HttpResponseRedirect(reverse("colleges", args=(email,)))

#Selection page loader
def secondPage(request, email, college_id, dname,id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("page2.html")
    college = College.objects.get(id=college_id)
    department = Department.objects.get(name=dname, college_main_id=college_id, creator_id=user_id)
    departments = Department.objects.filter(college_main_id=college_id)
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
                HttpResponseRedirect(reverse('pagetwo',args=(college_id, dname, tp)))
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
        return HttpResponseRedirect(reverse('pagetwo',args=(email,college_id, dname, id)))
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
        "courses" : course, "departments" : departments,"college": college_id
        ,"ldept":lastdepartment, "result":result, "year_groups": year_groups,
          "dname": dname, "page" : page, "tp":tp, "department": department,
          "email":email,
    }
    return HttpResponse(template.render(context, request))


def viewSelected(request, college_id, email):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("vscourses.html")
    courses = Course.objects.filter(creator_id=user_id)
    departments = Department.objects.filter(college_main_id=college_id)
    year_groups = [i for i in range(1,20+1)]
    temp_list =[]
    for x in courses:
        if x.id in selected_courses:
            temp_list.append(x)
    print("temp list is : ", temp_list)
    context = {
        "y_gs": year_groups, "college":college_id, "departments": departments,
          "list":temp_list, "email":email
    }
    return HttpResponse(template.render(context, request))


#Timetable page loader
def generateTimetable(request, college_id, email):
    user_id = UserAccount.objects.get(email=email).id
    # college = College.objects.get(creater_id=user_id, name)
    if request.method == "POST":
        print("generating")
        Schedule.objects.filter(college_id=college_id).delete()
        for course_id in selected_courses:
            createSchedule(course_id=course_id, user_id=user_id)
    return HttpResponseRedirect(reverse("timetablePage", args=(email, college_id)))

def timetable(request, email, college_id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("timetablepage.html")
    schedule = Schedule.objects.filter(creator_id=user_id, college_id=college_id).order_by("row")
    course = Course.objects.all().values()
    departments = Department.objects.filter(college_main_id=college_id)
    max_yg = (departments.order_by("-max_yg").first()).max_yg
    college = College.objects.get(id=college_id)
    rows_per_day = college.rows_per_day
    days_per_week = college.days_per_week
    nofdepts = len(departments)
    days = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday"}
    year_groups = []
    ss =[]
    for sch in schedule:
        if sch.department in departments:
            ss.append(sch)
    scarr ={}
    nfds = len(departments) * college.rows_per_day
    row = list(" " * nfds)
    l1 = len(ss)
    for x in range(1, (max_yg * college.days_per_week +1)):
        scarr[x] = row
    temp = []
    tt =0
    for x in ss:
        group =(x.row // college.rows_per_day) + 1
        rem = x.row % college.rows_per_day
        position = round(((rem-1)*len(departments)) + (x.column-1))
        if x.row % college.rows_per_day == 0:
            group = (x.row // college.rows_per_day)
        temp = []
        temp = scarr[group].copy()
        temp[position] = x
        scarr[group] = temp
    times = {0:"PERIOD",1:"8:00 - 8:55", 2:"9:00 - 9:55", 3:"10:30 - 11:25", 4:"11:30 - 12:25", 5:"1:00 - 1:55", 6:"2:00 - 2:55", 7:"3:00 - 3:55", 8:"4:00 - 4:55", 9:"5:00 - 5:55", 10:"6:00 - 6:55", 11:"7:00 - 7:55", 12:"8:00 - 8:55", 13:"9:00 - 9:55", 14:"10:00 - 10:55"}
    print(year_groups)
    context = {
        "schedule": schedule, "departments": departments, "scarr": scarr, "days": days,
        "year_groups":year_groups, "times":times, "college":college_id, "nofdepts":nofdepts,
        "email":email,"rows_per_day": rows_per_day, "days_per_week":days_per_week,
    }
    return HttpResponse(template.render(context, request))


def createCoursePage(request,email, department_id, year_group):
    user_id = UserAccount.objects.get(email=email).id
    course = Course.objects.filter(creator_id=user_id).values()
    template = loader.get_template("createcourse.html")
    department = Department.objects.get(id=department_id)
    college_id = department.college_main_id
    college = Department.objects.get(id=department_id).college
    slecturer = Lecturer.objects.all().order_by("surname")
    departments = Department.objects.all().filter(college=college).order_by("name")

    if request.method == "POST":
        course=createCourse(dictionary=request.POST, user_id=user_id)
        return HttpResponseRedirect(reverse("createcourse2", args=(email, course.id)))
    context = {
        "lecturer": slecturer, "departments": departments, "department":department,
        "year_group": year_group, "email":email, "college_id":college_id
    }
    return HttpResponse(template.render(context, request))

def createCoursePage2(request, email, course_id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("createcourse2.html")
    course = Course.objects.get(id=course_id)
    department = Department.objects.get(id=course.department_id)
    if department.limited: locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size, floor=0)
    else: locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size)
    if request.method == "POST":
        dictionary = request.POST
        preferred_location_id = dictionary.get('location', False)
        if preferred_location_id:
            course.preferred_location_id = dictionary['location']
            course.save()
        return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
    context = {
        "course":course, "locations":locations,
        }
    return HttpResponse(template.render(context, request))

def deleteCourse(request, email, college, dname, year_group):
    if request.method =='POST':
        dictionary = dict(request.POST)
        dictionary.pop("csrfmiddlewaretoken")
        for x in dictionary.values():
            course_id = int(x[0])
            Course.objects.all().get(id=course_id).delete()
        return HttpResponseRedirect(reverse("pagetwo", args=(email,college,dname,year_group)))


def optionsPage(request, email, college_id, count):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("optionsPage.html")
    count = list(range(1,count+1))
    context = {
        "college_id": college_id, "count": count, "email":email,
    }
    return HttpResponse(template.render(context, request))

def viewDepartments(request, email, college_id):
    user_id = UserAccount.objects.get(email=email).id
    college = College.objects.get(id=college_id)
    template = loader.get_template("depts.html")
    if request.method =="POST":
        bb =dict(request.POST)
        bb.pop('csrfmiddlewaretoken')
        d = "department"
        d1 = 0
        c = "code"
        nums = 1
        m = "max_yg"
        m1 =0
        c1 = 0
        for x, y in list(bb.items()):
            dd = d + str(nums)
            cc = c + str(nums)
            mm = m + str(nums)
            if(x == dd):
                department = y[0].upper()
                d1 = d1 + 1
                continue
            if(x == cc):
                code = y[0].upper()
                c1 = c1 + 1
                continue
            if(x == mm):
                max_yg = y[0]
                m1 = m1 + 1
            if(d1==m1):
                if not Department.objects.filter(name=department,college=college.name, college_main_id=college_id):
                    new_Department = Department(name=department, code=code, college=college.name, max_yg=max_yg, college_main_id=college_id, creator_id=user_id)
                    new_Department.save()
            nums = nums + 1
    
    departments = Department.objects.filter(college_main_id=college_id)
    first_department = departments.filter().first()
    first_department_name = departments.filter().first().name
    
    context = {
        "departments": departments, "college_id" : college_id, "first": first_department_name,
        "max_yg" : first_department.max_yg, "email":email
    }
    return HttpResponse(template.render(context, request))



def editCourse(request, email, code, id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("editcourse.html")
    course = Course.objects.get(code=code, id=id)
    slecturer = Lecturer.objects.all().values()
    cdepartment = Department.objects.get(id=course.department_id)
    college_id = cdepartment.college_main_id
    if Location.objects.filter(id=course.preferred_location_id):
        pref_loc = Location.objects.get(id=course.preferred_location_id)
    else: pref_loc=""
    clecturer = Lecturer.objects.get(id=course.lecturer_id)
    departments = Department.objects.all().values()
    if cdepartment.limited: available_locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size, floor=0)
    else: available_locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size)
    bool_List = [True, False]
    if request.method == "POST":
        dictionary = request.POST
        mcourse = modifyCourse(course=course, dictionary=dictionary)
        mcourse.creator_id = user_id
        mcourse.save()
        return HttpResponseRedirect(reverse('pagetwo',args=(email, cdepartment.college_main_id, cdepartment.name, course.year_group)))

    context = {"course": course, "lecturer":slecturer, "departments": departments,
               "clecturer": clecturer, "cdepartment": cdepartment, "bool_List": bool_List,
               "email": email, "college_id": college_id, "available_locations":available_locations,
               "pref_loc":pref_loc,
               }
    return HttpResponse(template.render(context, request))

def createDepartment(request, email, college_id=1):
    creator_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("createdept.html")
    college_name = College.objects.get(id=college_id)
    if request.method == "POST":
        dictionary = request.POST
        name = dictionary['name'].upper()
        code = dictionary['code'].upper()
        max_yg = int(dictionary['max_yg'])
        new_Department = Department(
            name=name, college_main_id=college_id, college=college_name, code=code, max_yg=max_yg,
            creator_id=creator_id
            )
        new_Department.save()

    context = {"college_name":college_name}
    return HttpResponse(template.render(context, request))


def allLecturers(request, email):
    template = loader.get_template("alllecturers.html")
    creator_id = UserAccount.objects.get(email=email).id
    departments = Department.objects.filter(creator_id=creator_id)
    lecturers = Lecturer.objects.filter(creator_id=creator_id).order_by("other_names")
    context = {
        "lecturers":lecturers, "departments":departments, "email":email
    }
    return HttpResponse(template.render(context, request))

def deleteLecturer(request, email, id):
    if request.method == "POST":
        current_lecturer = Lecturer.objects.get(id=id)
        current_lecturer.delete()
        return HttpResponseRedirect(reverse("alllecturers", args=(email,)))

def createLecturer(request, email):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("createlecturer.html")
    departments = Department.objects.filter(creator_id=user_id).values()
    if request.method == "POST":
        dictionary = request.POST
        surname = dictionary['surname'].capitalize()
        other_names = dictionary['other_names'].upper()
        department = dictionary['department']
        telephone = dictionary['telephone']
        email = dictionary['email']
        creator_id = UserAccount.objects.get(email=email).id
        new_Lecturer = Lecturer(email=email, telephone=telephone, creator_id=creator_id, surname=surname, other_names=other_names, department_id=department)
        new_Lecturer.save()
    context = {
        "departments": departments, "email":email,
    }
    return HttpResponse(template.render(context, request))

def modifyLecturerPage(request,email, lecturer_id):
    currentlect = Lecturer.objects.get(id=lecturer_id)
    department = Department.objects.get(id=currentlect.department_id)
    departments = Department.objects.all()
    template = loader.get_template("modifylect.html")
    if request.method == "POST":
        dictionary = request.POST
        modifylecturer(lecturer_id=lecturer_id, dictionary=dictionary)
        return HttpResponseRedirect(reverse('alllecturers', args=(email,)))
    context = {
        "currentlect":currentlect, "departments":departments, "department":department
    }
    return HttpResponse(template.render(context, request))

def locations(request,email):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("all-locations.html")
    locations = Location.objects.filter(creator_id=user_id).order_by("name")
    departments = Department.objects.filter(creator_id=user_id).order_by("name")
    number = len(locations)
    context = {
        "locations":locations, "departments":departments, "number": number,
        "email": email,
    }
    return HttpResponse(template.render(context, request))

def deleteLocation(request, email, id):
    if request.method == "POST":
        current_location = Location.objects.get(id=id)
        current_location.delete()
        return HttpResponseRedirect(reverse("locations", args=(email,)))


def addalocation(request, email):
    creator_id = UserAccount.objects.get(email=email).id
    if request.method == "POST":
        dictionary = request.POST
        name = dictionary['name'].upper()
        capacity = int(dictionary['capacity'])
        about = dictionary['about'].capitalize()
        is_in_same_college = dictionary.get('is_in_same_college', False)
        college = dictionary['college'].upper()
        floor = int(dictionary['floor'])
        college_main_id = College.objects.get(creater_id=creator_id, name__istartswith=college).id
        new_location = Location(
            floor=floor, college_main_id=college_main_id, creator_id=creator_id, college=college, name=name, capacity=capacity, about=about, is_in_same_college=is_in_same_college
        )
        new_location.save()
    return HttpResponseRedirect(reverse('locations', args=(email,)))

def modifylocation(request, email, id):
    user_id = UserAccount.objects.get(email=email).id
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
        currentlocation.college = dictionary['college'].upper()
        currentlocation.creator_id = user_id
        currentlocation.save()
        return HttpResponseRedirect(reverse("locations", args=(email,)))
    context = {
        'location':location, "boolist":boolist, "email":email,
    }
    return HttpResponse(template.render(context, request))


def deleteDepartment(request, email, id):
    if request.method == "POST":
        current_department = Department.objects.get(id=id)
        current_department.delete()
        return HttpResponseRedirect(reverse("alllecturers", args=(email,)))