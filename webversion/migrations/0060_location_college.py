# Generated by Django 5.0.6 on 2024-06-22 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0059_alter_department_max_yg'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='college',
            field=models.CharField(max_length=255, null=True),
        ),
    ]