from rest_framework import serializers
from ..models import *

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            'id', 'course', 'course_code', 'year_group', 'location',
            'location_name', 'column', 'row', 'department',
            'lecturer_name', 'lecturer', 'college',
            )
    