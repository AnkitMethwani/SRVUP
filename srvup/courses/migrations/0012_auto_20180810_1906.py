# Generated by Django 2.0.7 on 2018-08-10 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20180810_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='categor',
            new_name='category',
        ),
    ]
