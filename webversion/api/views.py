from rest_framework import viewsets
from ..models import Schedule, Course
from .serializers import ScheduleSerializer, CourseSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    # def get_queryset(self):
    #     # course_id  = self.request.user
    #     # return Course.objects.filter(id=course_id)
    #     course_id = self.kwargs['course_id']
    #     return Course.objects.filter(id=course_id)