# Generated by Django 4.2.14 on 2024-07-17 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0076_schedule_day_schedule_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='batch',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='college_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]