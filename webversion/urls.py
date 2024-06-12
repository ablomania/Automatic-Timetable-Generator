from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('select/<str:college>/<str:dname>/<int:id>', views.secondPage, name='pagetwo'),
    path("<str:college>/timetable",views.timetable, name="timetablePage"),
    path("createcourse", views.createCourse, name="createCourse"),
    path("editcourse", views.editCourse, name="editCourse")
]