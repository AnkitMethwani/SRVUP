# Generated by Django 2.0.7 on 2018-08-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_mycourses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycourses',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='owned', to='courses.Course'),
        ),
    ]
