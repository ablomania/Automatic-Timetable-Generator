# Generated by Django 5.0.6 on 2024-06-15 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0055_rename_location_schedule_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_comnined',
            field=models.BooleanField(default=False, null=True),
        ),
    ]