# Generated by Django 5.0.6 on 2024-06-15 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0054_alter_department_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='Location',
            new_name='location',
        ),
    ]
