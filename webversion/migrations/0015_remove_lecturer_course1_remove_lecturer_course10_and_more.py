# Generated by Django 5.0.6 on 2024-05-26 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0014_course_lecturer1_course_lecturer10_course_lecturer2_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='course1',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course10',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course2',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course3',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course4',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course5',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course6',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course7',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course8',
        ),
        migrations.RemoveField(
            model_name='lecturer',
            name='course9',
        ),
    ]