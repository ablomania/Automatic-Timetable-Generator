# Generated by Django 4.2.14 on 2024-07-30 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0093_examschedule_department_examschedule_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='examschedule',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='examcollege', to='webversion.college'),
        ),
        migrations.AddField(
            model_name='examschedule',
            name='college_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]