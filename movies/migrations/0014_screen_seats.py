# Generated by Django 2.1 on 2018-11-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_movie_synopsis'),
    ]

    operations = [
        migrations.AddField(
            model_name='screen',
            name='seats',
            field=models.ManyToManyField(to='movies.Seat'),
        ),
    ]