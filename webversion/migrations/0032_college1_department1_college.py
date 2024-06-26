# Generated by Django 5.0.6 on 2024-05-30 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0031_course1_lecturer1_department1_course1_lecturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='College1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='department1',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='college', to='webversion.college1'),
        ),
    ]
