# Generated by Django 2.1 on 2018-11-05 05:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_remove_movie_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(seconds=7200)),
        ),
    ]