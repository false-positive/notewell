# Generated by Django 3.2.6 on 2021-08-18 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0013_auto_20210812_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=64, verbose_name='Title'),
        ),
    ]
