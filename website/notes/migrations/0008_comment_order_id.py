# Generated by Django 3.2.5 on 2021-07-16 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0007_bulletpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='order_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]