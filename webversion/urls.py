from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('select/<str:college>/<str:dname>/<int:id>', views.secondPage, name='pagetwo'),
    path("<str:college>/timetable",views.timetable, name="timetablePage"),
    path("addaCoursePage/<int:department_id>/<int:year_group>", views.createCoursePage, name="createCourse"),
    path("editcourse/<str:code>", views.editCourse, name="editCourse"),
    path("createDepartment", views.createDepartment, name="createDept"),
    path("createLecturer", views.createLecturer, name="createLecturer"),
    path("optionsPage", views.optionsPage, name="toBegin"),
    path("departments/<str:collegename>", views.viewDepartments, name="departments"),
    path("select/<str:college>/viewselected", views.viewSelected, name="viewSelected"),
    path("deletecourse/<str:college>/<str:dname>/<int:year_group>", views.deleteCourse, name="deletecourse"),
    path("locations", views.locations, name="locations"),
    path("modifylecturer/<int:lecturer_id>", views.modifyLecturerPage, name="modifylectuer"),
    path("alllecturers", views.allLecturers, name="alllecturers"),
    path("deletelecturer/<int:id>", views.deleteLecturer, name="deletelecturer"),
    path("deletedepartment/<int:id>", views.deleteDepartment, name="deletedepartment"),
    path("addlocation", views.addalocation, name="createlocation"),
    path("deletelocation/<int:id>", views.deleteLocation, name="deletelocation"),
    path("editlocation/<int:id>", views.modifylocation, name="modifylocation")
]