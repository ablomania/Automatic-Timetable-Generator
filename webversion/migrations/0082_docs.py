# Generated by Django 4.2.14 on 2024-07-21 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webversion', '0081_schedule_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.PositiveBigIntegerField()),
                ('file', models.FileField(upload_to='docx')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docx_college', to='webversion.college')),
            ],
        ),
    ]