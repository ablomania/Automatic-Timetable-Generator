# Generated by Django 5.0.6 on 2024-05-30 19:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0038_remove_department_year_group_course_year_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveSmallIntegerField(null=True)),
                ('Location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alocation', to='webversion.location')),
                ('course_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acourse', to='webversion.course')),
            ],
        ),
    ]
