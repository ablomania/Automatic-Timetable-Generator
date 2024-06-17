from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('select/<str:college>/<str:dname>/<int:id>', views.secondPage, name='pagetwo'),
    path("<str:college>/timetable",views.timetable, name="timetablePage"),
    path("addaCoursePage", views.createCoursePage, name="createCourse"),
    path("editcourse/<str:code>", views.editCourse, name="editCourse"),
    path("createDepartment", views.createDepartment, name="createDept"),
    path("createLecturer", views.createLecturer, name="createLecturer"),
    path("optionsPage", views.optionsPage, name="toBegin"),
    path("departments/<str:collegename>", views.viewDepartments, name="departments"),
    path("select/<str:college>/<str:dname>/viewselected", views.viewSelected, name="viewSelected")
]