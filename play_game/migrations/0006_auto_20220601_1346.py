# Generated by Django 2.2 on 2022-06-01 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('play_game', '0005_auto_20220601_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamecreator',
            old_name='date_started',
            new_name='timestamp',
        ),
    ]