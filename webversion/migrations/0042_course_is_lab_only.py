# Generated by Django 5.0.6 on 2024-06-01 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0041_schedule_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_lab_only',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
