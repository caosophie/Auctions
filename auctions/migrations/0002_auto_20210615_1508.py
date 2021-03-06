# Generated by Django 3.2.3 on 2021-06-15 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activelisting',
            old_name='object',
            new_name='category',
        ),
        migrations.AddField(
            model_name='activelisting',
            name='bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activelisting',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
