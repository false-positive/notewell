# Generated by Django 3.2.6 on 2021-08-26 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0019_alter_category_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BulletPoint',
        ),
    ]