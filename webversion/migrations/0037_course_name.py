# Generated by Django 5.0.6 on 2024-05-30 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0036_remove_programme_dept_remove_course_programme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
