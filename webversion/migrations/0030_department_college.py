# Generated by Django 5.0.6 on 2024-05-28 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0029_remove_lecture_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='college',
            field=models.CharField(max_length=255, null=True),
        ),
    ]