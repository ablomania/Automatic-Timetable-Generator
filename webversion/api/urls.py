from rest_framework import routers
from .views import ScheduleViewSet,CourseViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'schedules', ScheduleViewSet)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]