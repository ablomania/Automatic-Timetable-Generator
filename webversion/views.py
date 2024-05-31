from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .models import Lecturer, Location, Department, Course,Schedule
import json 

# Create your views here.

def homePage(request):
    template = loader.get_template("index.html")
    context = {

    }
    return HttpResponse(template.render(context, request))



# aa = Programme.objects.get(code ="AERO", year_group = 1)
# bb = Lecture.objects.filter(programme_id = 6).values()
# course =Course.objects.all().values()
# print(bb)
# print()
# print(course)
department = Department.objects.get(name="Computer")
print(department)

def secondPage(request, college, dname,id):
    template = loader.get_template("page2.html")
    department = Department.objects.get(name=dname, college=college)
    departments = Department.objects.filter(college=college)
    course = Course.objects.filter(department_id = department.id, year_group=id)
    print("weeed")
    
    if request.method == 'POST':
        b = dict(request.POST)
        b.pop("csrfmiddlewaretoken")
        print(b)
        print(len(b))
        for x in b.values():
            new_schedule = Schedule(course_name_id = x[0])
            new_schedule.save()





    # if request.method == 'POST':
    #     name = request.POST['name']
    #     comment = request.POST['comment']
    #     new_comment = Usercomments(name=name, comnt=comment, relatedarticle_id = openarticle.id)
    #     new_comment.save()
    # openarticle.id = readerf



    lastdepartment = departments.filter().last().id
    firstdepartment = departments.filter().first().id
    page = 1 + id
    if(page == 5):
        d = department.id + 1
        dname = departments.get(id = d)
        page = 1
       
    
    tcourses = len(course)
    context = {
        "course" : course, "departments" : departments,"college": college
        , "dname": dname, "page" : page, "tcourses" : "tcourses"
    }
    return HttpResponse(template.render(context, request))



def timetable(request):
    template = loader.get_template("timetablepage.html")
    course = Course.objects.all().values()
    schedule = Schedule.objects.all().values()
    labs = course.filter(has_labs = True)
    location = Location.objects.all().values()
    time = range(8, 19)
    columns = range(1, 16)
    rows = range(1, 12)
    bb = list()
    for x in columns:
        for y in rows:
            bb.append(dict(column=x,row=y))
    print(bb)

    context = {

    }
    return HttpResponse(template.render(context, request))