# Generated by Django 3.2.8 on 2021-10-23 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0023_auto_20211023_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='date',
            new_name='creation_date',
        ),
    ]
