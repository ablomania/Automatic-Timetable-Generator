from django.contrib import admin
from .models import UserAccount, College, Course, Location, Lecturer, Department, Schedule


# Register your models here.
# admin.site.register(Programme)
admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Schedule)
admin.site.register(Lecturer)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(UserAccount)


