from rest_framework import viewsets, generics
from ..models import Schedule, Course, Timetable, College, Department
from .serializers import ScheduleSerializer, CourseSerializer, TimetableSerializer, DepartmentSerializer, CollegeSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        year_group = self.request.query_params.get('year_group')
        department_id = self.request.query_params.get('department_id')
        timetable_id = self.request.query_params.get('timetable_id')
        return Schedule.objects.filter(year_group=year_group, department_id=department_id, timetable_id=timetable_id)

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer

    def get_queryset(self):
        # Replace 'your_specific_code_value' with the actual code you're filtering by
        code = self.request.query_params.get('code')
        return Timetable.objects.filter(code=code)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        college_main_id = self.request.query_params.get('college_main_id')
        return Department.objects.filter(college_main_id=college_main_id)
    

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

    def get_queryset(self):
        college_id = self.request.query_params.get('id')
        print(college_id)
        return College.objects.filter(id=college_id)


