# Generated by Django 5.0.6 on 2024-06-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0043_course_is_electtive'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='estimated_class_size',
            field=models.PositiveIntegerField(default=200, null=True),
        ),
    ]