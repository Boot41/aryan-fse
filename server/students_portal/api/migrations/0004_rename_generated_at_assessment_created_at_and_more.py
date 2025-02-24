# Generated by Django 5.1.6 on 2025-02-24 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_profile_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assessment',
            old_name='generated_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='assessment',
            name='test_data',
        ),
        migrations.AddField(
            model_name='assessment',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='duration',
            field=models.CharField(default='30 minutes', max_length=50),
        ),
        migrations.AddField(
            model_name='assessment',
            name='scheduled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20),
        ),
        migrations.AddField(
            model_name='assessment',
            name='title',
            field=models.CharField(default='Untitled Assessment', max_length=255),
        ),
        migrations.AddField(
            model_name='assessment',
            name='total_questions',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='assessment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='chatbotinteraction',
            name='conversation_status',
            field=models.CharField(choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20),
        ),
        migrations.AddField(
            model_name='chatbotinteraction',
            name='conversation_topic',
            field=models.CharField(blank=True, help_text='The specific topic being discussed in this conversation', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='chatbotinteraction',
            name='topic_proficiency',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Student proficiency in the topic (0-100)', max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='result',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='chatbotinteraction',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chatbot_interactions', to='api.subject'),
        ),
    ]
