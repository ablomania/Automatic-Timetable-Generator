# Generated by Django 5.0.6 on 2024-05-26 08:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0011_delete_coursetolecturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='webversion.programme'),
        ),
    ]
