# Generated by Django 5.0.6 on 2024-05-26 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0016_rename_programme1_course_programme_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='programme',
        ),
        migrations.AddField(
            model_name='lecturer',
            name='programme1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme1', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='programme2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme2', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='programme3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme3', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='programme4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme4', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='programme5',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme5', to='webversion.programme'),
        ),
    ]
