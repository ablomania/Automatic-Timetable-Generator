from django.db import models

# Create your models here. 
class UserAccount(models.Model):
    email = models.EmailField(null=True, max_length=255)
    password = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f"{self.email}"

class College(models.Model):
    name = models.CharField(null=True,max_length=255)
    creater = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="college_user")
    rows_per_day = models.PositiveSmallIntegerField(null=True)
    days_per_week = models.PositiveSmallIntegerField(null=True)
    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=255, null=True)
    lecturer = models.ForeignKey("Lecturer", on_delete=models.CASCADE, related_name="alecturer", null=True)
    department = models.ForeignKey("Department", on_delete=models.CASCADE, related_name="adepartment", null=True)
    hours = models.PositiveSmallIntegerField(default=2, null=True)
    has_labs = models.BooleanField(default=False, null=True)
    is_combined = models.BooleanField(default=False, null=True)
    is_lab_only = models.BooleanField(default=False, null=True)
    is_elective = models.BooleanField(default=False, null=True)
    lab_hours = models.PositiveSmallIntegerField(default=0, null=True)
    is_contiguous_lab_time = models.BooleanField(default=0, null=True)
    year_group = models.PositiveSmallIntegerField(null=True)
    estimated_class_size = models.PositiveIntegerField(default=200, null=True)
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="course_creator", null=True)
    preferred_location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="course_location", null=True)
    def __str__(self):
        return f"{self.code} - {self.name}"


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(default=0)
    is_Lab = models.BooleanField(default=False, null=True)
    about = models.CharField(max_length=255, null=True)
    is_in_same_college = models.BooleanField(default=True, null=True)
    college_main = models.ForeignKey("College", on_delete=models.CASCADE, related_name="location_college", null=True)
    college = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="location_creator", null=True)
    floor = models.SmallIntegerField(null=True)
    def __str__(self):
        return f"{self.name}"
    

class Lecturer(models.Model):
    surname = models.CharField(max_length=255, null=True)
    other_names = models.CharField(max_length=255, null=True)
    department = models.ForeignKey("Department", on_delete=models.CASCADE, related_name="department")
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="lecturer_creator", null=True)
    email = models.EmailField(null=True)
    telephone = models.CharField(max_length=15, null=True)
    time_preference = models.PositiveSmallIntegerField(null=True)
    
    def __str__(self):
        return f"{self.other_names} {self.surname}"
    

class Schedule(models.Model):
    course= models.ForeignKey("Course", on_delete=models.CASCADE, related_name="acourse", null=True)
    course_code = models.CharField(max_length=50, null=True)
    year_group = models.PositiveSmallIntegerField(null = True)
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="alocation", null=True)
    location_name = models.CharField(max_length=255, null = True)
    height = models.PositiveSmallIntegerField(null=True)
    column = models.PositiveSmallIntegerField(null=True)
    row = models.PositiveSmallIntegerField(null=True)
    department =models.ForeignKey("Department", on_delete=models.CASCADE, related_name="somedepartment", null=True)
    lecturer_name = models.CharField(max_length=255, null=True)
    lecturer = models.ForeignKey("Lecturer", on_delete=models.CASCADE, related_name="the_lecturer", null=True)
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="schedule_creator", null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="schedule_college", null=True)
    def __str__(self):
        return f"{self.course_code} {self.location_name} {self.lecturer_name}"

class Department(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=50, null=True)
    college_main = models.ForeignKey("College", on_delete=models.CASCADE, related_name="department_college", null=True)
    college = models.CharField(max_length=255, null=True)
    max_yg = models.PositiveSmallIntegerField(default=4, null=True)
    creator = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="department_creator", null=True)
    limited = models.BooleanField(null=True)
    def __str__(self):
        return f"{self.name}"

    
# class Lecture(models.Model):
#     # name = models.CharField(max_length=255)
#     # department = models.ForeignKey("Programme", on_delete=models.CASCADE, related_name='department', null=True)
#     course  = models.ForeignKey("Course", on_delete=models.CASCADE, related_name='course', null=True)
#     programme = models.ForeignKey("Programme", on_delete=models.CASCADE, related_name="programme", null=True)
#     lecturer = models.ForeignKey("Lecturer", on_delete=models.CASCADE, related_name="lecturer", null=True)
#     def __str__(self):
#         return f"{self.course} + {self.lecturer}"
