# Generated by Django 5.1.6 on 2025-02-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_assignment_duration_assignment_total_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentassignment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
