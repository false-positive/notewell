# Generated by Django 3.2.6 on 2021-08-12 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0011_note_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
