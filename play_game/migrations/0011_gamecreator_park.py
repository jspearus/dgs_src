# Generated by Django 2.2 on 2022-06-05 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('play_game', '0010_auto_20220605_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamecreator',
            name='park',
            field=models.CharField(default='park', max_length=140),
            preserve_default=False,
        ),
    ]
