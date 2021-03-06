# Generated by Django 2.2 on 2022-06-01 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('play_game', '0006_auto_20220601_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentgame',
            name='cur_hole',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gamecreator',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
