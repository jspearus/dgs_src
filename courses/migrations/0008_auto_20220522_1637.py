# Generated by Django 2.2 on 2022-05-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20220522_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holecreater',
            name='distance',
            field=models.IntegerField(default=250),
        ),
        migrations.AlterField(
            model_name='holecreater',
            name='par',
            field=models.IntegerField(default=3),
        ),
    ]