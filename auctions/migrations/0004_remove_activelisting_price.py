# Generated by Django 3.2.3 on 2021-06-27 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210627_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activelisting',
            name='price',
        ),
    ]
