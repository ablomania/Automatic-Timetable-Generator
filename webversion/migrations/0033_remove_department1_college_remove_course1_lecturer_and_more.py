# Generated by Django 5.0.6 on 2024-05-30 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0032_college1_department1_college'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department1',
            name='college',
        ),
        migrations.RemoveField(
            model_name='course1',
            name='lecturer',
        ),
        migrations.RemoveField(
            model_name='department1',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='has_labs',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='lab_hours',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='College1',
        ),
        migrations.DeleteModel(
            name='Lecturer1',
        ),
        migrations.DeleteModel(
            name='Course1',
        ),
        migrations.DeleteModel(
            name='Department1',
        ),
    ]
