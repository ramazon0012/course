# Generated by Django 5.0 on 2024-03-13 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_course_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='poster',
            field=models.ImageField(default=1, upload_to='posters/'),
            preserve_default=False,
        ),
    ]
