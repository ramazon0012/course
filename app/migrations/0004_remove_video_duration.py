# Generated by Django 4.1.6 on 2024-02-24 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_video_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='duration',
        ),
    ]
