# Generated by Django 5.0.6 on 2024-05-26 08:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0012_lecturer_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='programme',
        ),
        migrations.AddField(
            model_name='course',
            name='programme1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme1', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme10',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme10', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme2', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme3', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme4', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme5',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme5', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme6',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme6', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme7',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme7', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme8',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme8', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='course',
            name='programme9',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme9', to='webversion.programme'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course1', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course10',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course10', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course2', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course3', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course4', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course5',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course5', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course6',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course6', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course7',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course7', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course8',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course8', to='webversion.course'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='course9',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course9', to='webversion.course'),
        ),
    ]
