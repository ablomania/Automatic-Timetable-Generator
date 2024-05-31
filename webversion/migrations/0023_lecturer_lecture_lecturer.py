# Generated by Django 5.0.6 on 2024-05-27 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0022_rename_lecturer_lecture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=255, null=True)),
                ('other_names', models.CharField(max_length=255, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department', to='webversion.programme')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='lecturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lecturer', to='webversion.lecturer'),
        ),
    ]
