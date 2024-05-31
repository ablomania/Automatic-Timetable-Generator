from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('select/<str:college>/<str:dname>/<int:id>', views.secondPage, name='pagetwo'),
    path("timetable",views.timetable, name="timetablePage"),
]