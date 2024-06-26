# Generated by Django 5.0.6 on 2024-05-30 09:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0035_remove_course_is_combined_course_lecturer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programme',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme',
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adepartment', to='webversion.department'),
        ),
        migrations.AddField(
            model_name='department',
            name='year_group',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Lecture',
        ),
        migrations.DeleteModel(
            name='Programme',
        ),
    ]
