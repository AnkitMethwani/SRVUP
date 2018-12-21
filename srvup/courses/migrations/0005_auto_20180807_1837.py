# Generated by Django 2.0.7 on 2018-08-07 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_lecture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='lecture',
            unique_together={('slug', 'course')},
        ),
    ]