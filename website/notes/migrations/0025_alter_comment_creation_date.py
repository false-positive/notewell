# Generated by Django 3.2.8 on 2021-10-23 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0024_rename_date_comment_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]