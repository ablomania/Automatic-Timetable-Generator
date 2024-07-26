from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import UserAccount, Pref_location, Pref_day, Pref_time, College, Lecturer, Location, Department, Course, Schedule, Pref_Stuff, Docs, Timetable
from .functions import *
from .tablegen import tablegenerator
import random
import docx
from docx.shared import Mm
from docx.enum.section import WD_ORIENT
from pathlib import Path
from django.core.files import File
from django.http import FileResponse
from docx2pdf import convert
import time
from .pdfgen import createPdf


# Create your views here.
global selected_courses
# global preferred_List
selected_courses = []
# preferred_List = []
#Homepage loader
def homePage(request, error=0):
    template = loader.get_template("index.html")
    # emails = list(dict(UserAccount.objects.values_list("email", "password")))
    error = userEmail = password = 0
    print(error)
    if request.method == "POST":
        dictionary = request.POST
        userEmail = dictionary['email'].lower()
        password= dictionary['password']
        check_user = UserAccount.objects.filter(email=userEmail, password=password)
        if check_user:
            return HttpResponseRedirect(reverse("colleges", args=(userEmail,)))
        else:
           error = 1
           print(error)
    context = {
        "error":error, "userEmail":userEmail, "password":password,
    }
    return HttpResponse(template.render(context, request))


def createAccountPage(request):
    template = loader.get_template("create-account.html")
    emails = UserAccount.objects.all().values()
    error = new_email = 0
    if request.method == "POST":
        dictionary = request.POST
        new_email = dictionary['email']
        new_password = dictionary['password']
        check_user = UserAccount.objects.filter(email=new_email)
        if len(check_user) < 1:
            new_user = UserAccount(email=new_email, password=new_password)
            new_user.save()
            return HttpResponseRedirect(reverse("colleges", args=(new_email,)))
        else: error = 1
    context = {
        "error":error, "emails":emails, "new_email":new_email,
    }
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
    locations = Location.objects.filter(creator_id=user_id)
    if request.method == 'POST':
        b = dict(request.POST)
        b.pop("csrfmiddlewaretoken")
        for x in b.values():
            course_id = int(x[0])
            current_course = Course.objects.get(id=course_id)
            is_preferred = Pref_Stuff.objects.filter(course_id=course_id)
            if (current_course.has_labs or current_course.is_lab_only or len(is_preferred) > 0):
                selected_courses.insert(0, int(course_id))
            if(course_id not in selected_courses):
                selected_courses.append(int(course_id))
            if 'save' in request.POST:
                HttpResponseRedirect(reverse('pagetwo',args=(college_id, dname, tp)))
        print(selected_courses)
    result = {}
    for course_id in selected_courses:
        t = Course.objects.filter(id=course_id)
        if len(t) > 0:
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
          "email":email, "college_name":college.name,"n_locations":len(locations)
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
    preferred = list(dict(Pref_Stuff.objects.filter(college_main_id=college_id).values_list("course_id", "id")))
    is_batch = Timetable.objects.filter(batch__gte=1)
    preferred_List = lab_List = con_labs_List = []
    lab_courses = list(dict(Course.objects.filter(creator_id=user_id, has_labs=True).values_list("id", "name")))
    cc =list(dict(Course.objects.filter(creator_id=user_id, is_contiguous_lab_time=True).values_list("id", "name")))
    print("sc bf pl", selected_courses)
    for pref in list(preferred):
        if int(pref) in list(selected_courses):
            preferred_List.append(int(pref))
            selected_courses.remove(int(pref))
    print("pl", preferred_List)
    print("sc af pl", selected_courses)
    for slt in list(selected_courses):
        if int(slt) in list(cc): con_labs_List.append(int(slt))
        else:
            if int(slt) in list(lab_courses):
                lab_List.append(int(slt))
                selected_courses.remove(int(slt))
    print("ll", lab_List)
    print("sc af ll", selected_courses)
    for ll in list(lab_List):
        selected_courses.insert(0, int(ll))
    print("sc wt ll", selected_courses)
    for c in list(con_labs_List):
        if int(c) in list(selected_courses): selected_courses.remove(int(c))
        selected_courses.insert(0, int(c))
    for pl in list(preferred_List):
        if int(pl) in list(selected_courses): selected_courses.remove(int(pl))
        selected_courses.insert(0, int(pl))
    print("sc wt pl and ll", selected_courses)
    if len(is_batch) > 0: 
        batch = Timetable.objects.order_by("-batch").first().batch
        batch = batch + 1
    else: batch = 1
    code = 343256 + batch
    if request.method == "POST":
        new_timetable = Timetable(
            code=code, batch=batch, college_main_id=college_id
        )
        new_timetable.save()
        print("generating")
        # Schedule.objects.filter(college_id=college_id).delete()
        for course_id in selected_courses:
            createSchedule(course_id=course_id, user_id=user_id, timetable=new_timetable.id)
    return HttpResponseRedirect(reverse("collegeTables", args=(email, college_id)))
    # return HttpResponseRedirect(reverse("timetablePage", args=(email, college_id)))

def deleteTimetable(request, email, college_id, timetable_id):
    user_id = UserAccount.objects.get(email=email).id
    if request.method == "POST":
        target = Timetable.object.get(id=timetable_id)
        target.delete()
    return HttpResponseRedirect(reverse("collegeTables", args=(email, college_id)))

def collegeTimeTables(request, email, college_id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("collegetables.html")
    timetables = Timetable.objects.filter(college_main_id=college_id)
    college = College.objects.get(id=college_id)
    dates = []
    first_department = Department.objects.filter(college_main_id=college_id).order_by("name").first()
    
    context = {
        "timetables": timetables, "dates":dates, "college_name":college.name,
        "email": email, "college_id":college_id, "first_dept":first_department,
    }
    return HttpResponse(template.render(context, request))

def timetable(request, email, college_id,timetable_id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("timetablepage.html")
    schedule = Schedule.objects.filter(creator_id=user_id, college_id=college_id, timetable_id=timetable_id).order_by("row")
    course = Course.objects.all().values()
    departments = Department.objects.filter(college_main_id=college_id)
    batch = Timetable.objects.get(id=timetable_id).batch
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
    #########################
    tablegenerator(college_id=college_id, user_id=user_id,some_list=ss, batch=batch)
    #########################
    check_doc = Docs.objects.filter(table_id=timetable_id, college_id=college_id)
    if len(check_doc) > 0: new_doc = Docs.objects.filter(table_id=timetable_id, college_id=college_id)
    else:
        new_doc = Docs(table_id=timetable_id, college_id=college_id)
        new_doc.save()
    dd = Docs.objects.get(table_id=timetable_id, college_id=college_id)
    path = Path(f"{college.name}_{batch}.docx")
    # car = Car.objects.get(name="57 Chevy")
    with path.open(mode="rb") as f:
        dd.file = File(f, name=path.name)
        dd.save()
    context = {
        "schedule": schedule, "departments": departments, "scarr": scarr, "days": days,
        "year_groups":year_groups, "times":times, "college":college, "nofdepts":nofdepts,
        "email":email,"rows_per_day": rows_per_day, "days_per_week":days_per_week,
        "new_doc":new_doc, "batch":batch,
    }
    return HttpResponse(template.render(context, request))

def downloadPdf(request, email, college_id, timetable_id):
    batch = Timetable.objects.get(id=timetable_id).batch
    college = College.objects.get(id=college_id)
    doc = Docs.objects.get(college_id=college_id, table_id=timetable_id)
    createPdf(college_id=college_id, batch=batch, doc=doc)
    path = doc.pdf.path
    file_name = str(college.name) + "_" + str(batch)
    response = FileResponse(open(path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{college.name}_{batch}.pdf"'
    return response

def downloadDoc(request, email, college_id, timetable_id):
    batch = Timetable.objects.get(id=timetable_id).batch
    college = College.objects.get(id=college_id)
    doc = Docs.objects.get(college_id=college_id, table_id=timetable_id)
    path = doc.file.path
    file_name = str(college.name) + "_" + str(batch)
    response = FileResponse(open(path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{college.name}_{batch}.docx"'
    return response


def createCoursePage(request,email, department_id, year_group):
    user_id = UserAccount.objects.get(email=email).id
    course = Course.objects.filter(creator_id=user_id).values()
    template = loader.get_template("createcourse.html")
    department = Department.objects.get(id=department_id)
    college_id = department.college_main_id
    college = Department.objects.get(id=department_id).college
    slecturer = Lecturer.objects.filter(creator_id=user_id).order_by("surname")
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
    college_id = department.college_main_id
    if department.limited: locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size, floor=0)
    else: locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size)
    number_of_schedules = int(math.ceil(course.hours / 2))
    times = ['8am','10:30am', '1pm', '3pm','5pm', '7pm', '9pm']
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    error = False
    if request.method == "POST":
        dictionary = dict(request.POST)
        preferred_location_id = dictionary.get('preferred_location', False)
        preferred_day = dictionary.get('preferred_day', False)
        preferred_time = dictionary.get('preferred_time', False)
        times = ['8am','9am','10:30am','11:30am', '1pm', '2pm', '3pm','4pm','5pm', '6pm', '7pm','8pm', '9pm', '10pm']
        if preferred_location_id: pref_location_id = dictionary['preferred_location']
        if preferred_day: preferred_day = list(dictionary['preferred_day'])
        if preferred_time: preferred_time = list(dictionary['preferred_time'])
        if "" in preferred_time or "" in preferred_location_id or "" in preferred_day:
            return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
        for time in list(preferred_time):
            for day in (preferred_day):
                for location in list(pref_location_id):
                    time_location_checker = Pref_Stuff.objects.filter(time=time, location_id=location, day=day)
                    print("tl ", time_location_checker)
                    if time_location_checker: 
                        error = {(Location.objects.get(id=location).name):times[int(time)]}
        if not error:
            if "" in preferred_time or "" in preferred_location_id or "" in preferred_day:
                return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
            else:
                count = 0
                for sch in range(number_of_schedules):
                    new_pref_stuff = Pref_Stuff(
                        time=preferred_time[count],
                        course_id=course_id,
                        day=preferred_day[count],
                        location_id=pref_location_id[count],
                        creator_id=user_id,
                        college_main_id = college_id
                    )
                    new_pref_stuff.save()
                    count = count + 1
                return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
    context = {
        "course":course, "locations":locations, "n_schedules":range(number_of_schedules), "times":times,
        "error":error,
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
    college_name = College.objects.get(id=college_id).name
    count = list(range(1,count+1))
    context = {
        "college_id": college_id, "count": count, "email":email,
        "college_name":college_name,
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
        "max_yg" : first_department.max_yg, "email":email, "college":college.name
    }
    return HttpResponse(template.render(context, request))



def editCourse(request, email, code, id):
    user_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("editcourse.html")
    course = Course.objects.get(code=code, id=id)
    slecturer = Lecturer.objects.filter(creator_id=user_id)
    cdepartment = Department.objects.get(id=course.department_id)
    college_id = cdepartment.college_main_id
    clecturer = Lecturer.objects.get(id=course.lecturer_id)
    departments = Department.objects.all().values()
    if cdepartment.limited: available_locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size, floor=0)
    else: available_locations = Location.objects.filter(creator_id=user_id, capacity__gte=course.estimated_class_size)
    preferred_location_list =[]
    bool_List = [True, False]
    if request.method == "POST":
        dictionary = request.POST
        mcourse = modifyCourse(course=course, dictionary=dictionary)
        mcourse.creator_id = user_id
        mcourse.save()
        return HttpResponseRedirect(reverse('editCourse2',args=(email, course.id)))

    context = {"course": course, "lecturer":slecturer, "departments": departments,
               "clecturer": clecturer, "cdepartment": cdepartment, "bool_List": bool_List,
               "email": email, "college_id": college_id, "available_locations":available_locations,
               "preferred_location_list":preferred_location_list,
               }
    return HttpResponse(template.render(context, request))

def editCourse2(request, email, id):
    template = loader.get_template("editCourse2.html")
    course = Course.objects.get(id=id)
    department_id = course.department_id
    department = Department.objects.get(id=department_id)
    college_id = department.college_main_id
    user_id = UserAccount.objects.get(email=email).id
    preferred = Pref_Stuff.objects.filter(creator_id=user_id, course_id=course.id, college_main_id=college_id)
    available_locations = list(Location.objects.filter(creator_id=user_id, capacity__gte=int(course.estimated_class_size)))
    number_of_schedules = int(math.ceil(course.hours / 2))
    range_of_sch = [i for i in range(number_of_schedules)]
    times = {1:'8am', 3:'10:30am', 5:'1pm', 7:'3pm', 9:'5pm', 11:'7pm', 13:'9pm'}
    days = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday'}
    # days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    error =  False
    ignoreError = 0
    if request.method == "POST":
        times = {1:'8am', 3:'10:30am', 5:'1pm', 7:'3pm', 9:'5pm', 11:'7pm', 13:'9pm'}
        days = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday'}
        dictionary = dict(request.POST)
        preferred_location_id = dictionary.get('preferred_location', False)
        preferred_day = dictionary.get('preferred_day', False)
        preferred_time = dictionary.get('preferred_time', False)
        if "" in preferred_time or "" in preferred_location_id or "" in preferred_day:
            return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
        for time in list(preferred_time):
            for day in (preferred_day):
                for location in list(preferred_location_id):
                    time_location_checker = Pref_Stuff.objects.filter(time=time, location_id=location, day=day)
                    for chk2 in time_location_checker:
                        if course.id == chk2.course_id: ignoreError = 1
                    if ignoreError < 1: error = {(Location.objects.get(id=location).name):times[int(time)]}
        if error is False and ignoreError > 0:
            return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
        else:
            if "" in preferred_time or "" in preferred_location_id or "" in preferred_day:
                return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
            else:
                count = 0
                for sch in range(number_of_schedules):
                    new_pref_stuff = Pref_Stuff(
                        time=preferred_time[count],
                        course_id=course.id,
                        day=preferred_day[count],
                        location_id=preferred_location_id[count],
                        creator_id=user_id,
                        college_main_id = college_id
                    )
                    if preferred: preferred.delete()
                    new_pref_stuff.save()
                    print("count is ", count)
                    count = count + 1
            return HttpResponseRedirect(reverse("pagetwo", args=(email, department.college_main_id, department.name, course.year_group)))
    context = {
        "course":course, "n_schedules": range_of_sch, "error": error,
        "times":times, "days":days,"available_locations":available_locations, 
        "preferred":preferred,
    }
    return HttpResponse(template.render(context, request))


def createDepartment(request, email, college_id, callingpage):
    creator_id = UserAccount.objects.get(email=email).id
    template = loader.get_template("createdept.html")
    college = College.objects.get(id=college_id)
    colleges = College.objects.filter(creater_id=creator_id)
    if request.method == "POST":
        dictionary = request.POST
        name = dictionary['name'].upper()
        code = dictionary['code'].upper()
        max_yg = int(dictionary['max_yg'])
        college_id_input = dictionary['college']
        limited_input = dictionary['limited']
        new_Department = Department(
            name=name, college_main_id=college_id_input, college=college.name, code=code, max_yg=max_yg,
            creator_id=creator_id
            )
        new_Department.save()
        if callingpage == "pagetwo":
            arg1 = email
            arg2 = college_id
            arg3 = new_Department.name
            arg4 = max_yg
            return HttpResponseRedirect(reverse(callingpage, args=(arg1, arg2, arg3, arg4)))
        elif callingpage == "colleges":
            arg1 = email
            return HttpResponseRedirect(reverse(callingpage, args=(arg1,)))
        elif callingpage == "alllecturers":
            arg1 = email
            return HttpResponseRedirect(reverse(callingpage, args=(arg1,)))
    context = {"college":college, "colleges":colleges,
               }
    return HttpResponse(template.render(context, request))


def allLecturers(request, email):
    template = loader.get_template("alllecturers.html")
    creator_id = UserAccount.objects.get(email=email).id
    departments = Department.objects.filter(creator_id=creator_id)
    lecturers = Lecturer.objects.filter(creator_id=creator_id).order_by("other_names")
    context = {
        "lecturers":lecturers, "departments":departments, "email":email,
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
    departments = Department.objects.filter(creator_id=user_id).order_by("college_main_id")
    if request.method == "POST":
        dictionary = request.POST
        surname = dictionary['surname'].capitalize()
        other_names = dictionary['other_names'].upper()
        department = dictionary['department']
        telephone = dictionary['telephone']
        email_input = dictionary['email']
        creator_id = UserAccount.objects.get(email=email).id
        new_Lecturer = Lecturer(email=email_input, telephone=telephone, creator_id=creator_id, surname=surname, other_names=other_names, department_id=department)
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
    colleges = College.objects.filter(creater=user_id)
    number = len(locations)
    context = {
        "locations":locations, "departments":departments, "number": number,
        "email": email, "colleges": colleges,
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
        college_main_id = int(dictionary['college'])
        floor = int(dictionary['floor'])
        college_name = College.objects.get(id=college_main_id).name
        new_location = Location(
            floor=floor, college_main_id=college_main_id, creator_id=creator_id, college=college_name, name=name, capacity=capacity, about=about, is_in_same_college=is_in_same_college
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