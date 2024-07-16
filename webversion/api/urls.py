from rest_framework import routers
from .views import ScheduleViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('', include(router.urls))
]