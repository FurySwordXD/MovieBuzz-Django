# Generated by Django 2.1 on 2018-11-05 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20181105_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='show',
            old_name='time',
            new_name='datetime',
        ),
    ]