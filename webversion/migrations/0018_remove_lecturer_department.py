# Generated by Django 5.0.6 on 2024-05-26 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0017_remove_course_programme_lecturer_programme1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='department',
        ),
    ]
