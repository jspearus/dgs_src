# Generated by Django 2.2 on 2022-05-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_holecreater_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holecreater',
            name='holeSub',
            field=models.CharField(default='A', max_length=1),
        ),
    ]
