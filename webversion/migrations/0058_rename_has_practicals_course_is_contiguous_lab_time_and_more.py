# Generated by Django 5.0.6 on 2024-06-19 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0057_rename_is_comnined_course_is_combined'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='has_practicals',
            new_name='is_contiguous_lab_time',
        ),
        migrations.RemoveField(
            model_name='course',
            name='practical_hours',
        ),
    ]