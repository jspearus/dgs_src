# Generated by Django 2.2 on 2022-06-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_game', '0004_auto_20220601_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamecreator',
            name='date_started',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]