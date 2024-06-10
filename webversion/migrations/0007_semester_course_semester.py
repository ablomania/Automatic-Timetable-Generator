# Generated by Django 5.0.6 on 2024-05-25 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0006_remove_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_sem', models.BooleanField()),
                ('second_sem', models.BooleanField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sem', to='webversion.semester'),
        ),
    ]