# Generated by Django 4.2.5 on 2023-12-03 20:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0009_beer_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyBeer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=25)),
                ('published_date', models.DateField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=30)),
                ('style', models.CharField(max_length=25)),
                ('alcohol_content', models.FloatField(default=0)),
                ('blg', models.FloatField(default=0)),
                ('picture', models.CharField(blank=True, max_length=250, null=True)),
                ('malts', models.TextField(blank=True, max_length=250, null=True)),
                ('hops', models.TextField(blank=True, max_length=250, null=True)),
                ('additives', models.TextField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
