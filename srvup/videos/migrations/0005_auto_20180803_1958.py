# Generated by Django 2.0.7 on 2018-08-03 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_video_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
