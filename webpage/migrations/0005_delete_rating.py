# Generated by Django 4.2.5 on 2023-11-28 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0004_remove_beer_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
