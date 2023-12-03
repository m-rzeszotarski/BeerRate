# Generated by Django 4.2.5 on 2023-10-10 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beer',
            old_name='date',
            new_name='published_date',
        ),
        migrations.AddField(
            model_name='beer',
            name='alcohol_content',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='beer',
            name='blg',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='beer',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]