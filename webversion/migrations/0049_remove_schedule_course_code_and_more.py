# Generated by Django 5.0.6 on 2024-06-10 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0048_schedule_course_code_schedule_year_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='course_code',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='year_group',
        ),
    ]
