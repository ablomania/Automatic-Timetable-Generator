# Generated by Django 5.0.6 on 2024-05-26 09:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0015_remove_lecturer_course1_remove_lecturer_course10_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='programme1',
            new_name='programme',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer1',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer10',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer2',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer3',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer4',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer5',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer6',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer7',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer8',
        ),
        migrations.RemoveField(
            model_name='course',
            name='lecturer9',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme10',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme2',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme3',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme4',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme5',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme6',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme7',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme8',
        ),
        migrations.RemoveField(
            model_name='course',
            name='programme9',
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c1', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c2', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c3', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c4', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course5',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c5', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='programme',
            name='year_group',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
