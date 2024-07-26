from rest_framework import routers
from .views import ScheduleViewSet,CourseViewSet, TimetableViewSet, DepartmentViewSet, CollegeViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'timetables', TimetableViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'colleges', CollegeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]