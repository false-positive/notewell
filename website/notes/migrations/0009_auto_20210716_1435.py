# Generated by Django 3.2.5 on 2021-07-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_comment_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='order_id',
        ),
        migrations.AddField(
            model_name='bulletpoint',
            name='order_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
