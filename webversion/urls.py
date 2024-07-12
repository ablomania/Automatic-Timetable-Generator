from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('<str:email>/select/<int:college_id>/<str:dname>/<int:id>', views.secondPage, name='pagetwo'),
    path("<str:email>/<int:college_id>/timetable",views.timetable, name="timetablePage"),
    path("<str:email>/addaCoursePage/<int:department_id>/<int:year_group>", views.createCoursePage, name="createCourse"),
    path("<str:email>/createcourse2/<int:course_id>", views.createCoursePage2, name="createcourse2"),
    path("<str:email>/editcourse/<str:code>/<int:id>", views.editCourse, name="editCourse"),
    path("<str:email>/editCourse2/<int:id>", views.editCourse2, name="editCourse2"),
    path("<str:email>/createDepartment/<int:college_id>/<str:callingpage>", views.createDepartment, name="createDept"),
    path("<str:email>/createLecturer", views.createLecturer, name="createLecturer"),
    path("<str:email>/optionsPage/<int:college_id>/<int:count>", views.optionsPage, name="toBegin"),
    path("<str:email>/departments/<int:college_id>", views.viewDepartments, name="departments"),
    path("<str:email>/select/<int:college_id>/viewselected", views.viewSelected, name="viewSelected"),
    path("<str:email>/deletecourse/<str:college>/<str:dname>/<int:year_group>", views.deleteCourse, name="deletecourse"),
    path("<str:email>/locations", views.locations, name="locations"),
    path("<str:email>/modifylecturer/<int:lecturer_id>", views.modifyLecturerPage, name="modifylecturer"),
    path("<str:email>/alllecturers", views.allLecturers, name="alllecturers"),
    path("<str:email>/deletelecturer/<int:id>", views.deleteLecturer, name="deletelecturer"),
    path("<str:email>/deletedepartment/<int:id>", views.deleteDepartment, name="deletedepartment"),
    path("<str:email>/addlocation", views.addalocation, name="createlocation"),
    path("<str:email>/deletelocation/<int:id>", views.deleteLocation, name="deletelocation"),
    path("<str:email>/editlocation/<int:id>", views.modifylocation, name="modifylocation"),
    path("<str:email>/generate-timetable/<int:college_id>", views.generateTimetable, name="generate"),
    path("<str:email>/colleges", views.collegePage, name="colleges"),
    path("<str:email>/deletecollege/<int:id>", views.deletecollege, name="deletecollege"),
    path("<str:email>/errorinput", views.errorInputPage, name="error-input"),
    path("createaccount", views.createAccountPage, name="create-account"),
    path("<str:email>/createcollege", views.createCollege, name="create-college"),
    path("<str:email>/collegeviewGenerator/<int:college_id>", views.collegeviewGenerator, name="collegeView"),
    path("<str:email>/editcollege/<int:college_id>", views.editcollege, name="editcollege")
]