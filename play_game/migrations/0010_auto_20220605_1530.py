# Generated by Django 2.2 on 2022-06-05 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play_game', '0009_gamesave'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamesave',
            options={'ordering': ['card', 'hole', 'holeSub']},
        ),
    ]
