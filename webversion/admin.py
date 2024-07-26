from django.contrib import admin
from .models import UserAccount, Pref_Stuff, Pref_day, Pref_location, Pref_time, College, Course, Location, Lecturer, Department, Schedule, Docs, Timetable


# Register your models here.
# admin.site.register(Programme)
admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Schedule)
admin.site.register(Lecturer)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(UserAccount)
admin.site.register(Pref_time)
admin.site.register(Pref_location)
admin.site.register(Pref_day)
admin.site.register(Pref_Stuff)
admin.site.register(Docs)
admin.site.register(Timetable)


