# Generated by Django 5.0.6 on 2024-05-26 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0019_remove_lecturer_course2_remove_lecturer_course3_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='course1',
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='webversion.course'),
        ),
    ]