# Generated by Django 2.2 on 2022-06-15 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20220614_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holecreater',
            name='basket',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='holecreater',
            name='holeSub',
            field=models.CharField(max_length=2),
        ),
    ]
