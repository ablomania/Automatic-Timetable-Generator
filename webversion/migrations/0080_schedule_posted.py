# Generated by Django 4.2.14 on 2024-07-20 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0079_alter_schedule_day_alter_schedule_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='posted',
            field=models.BooleanField(default=False),
        ),
    ]
