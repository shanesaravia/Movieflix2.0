# Generated by Django 2.0.1 on 2018-04-19 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movieflix', '0004_movie_poster'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='name',
            new_name='title',
        ),
    ]
