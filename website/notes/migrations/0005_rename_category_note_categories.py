# Generated by Django 3.2.5 on 2021-07-16 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_note_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='category',
            new_name='categories',
        ),
    ]
