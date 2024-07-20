from rest_framework import serializers
from ..models import *

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'id', 'course', 'course_code', 'year_group', 'location',
            'location_name', 'column', 'row', 'department',
            'lecturer_name', 'lecturer', 'college', 'time', 'day',
            'college_name'
            )

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'id', 'code', 'name', 'lecturer', 'department', 'hours',
            'has_labs', 'is_contiguous_class_time', 'is_lab_only',
            'lab_hours', 'is_contiguous_lab_time', 'year_group', 
            'estimated_class_size', 'creator'
        )
