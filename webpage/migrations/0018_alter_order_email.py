# Generated by Django 4.2.5 on 2023-12-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0017_order_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.CharField(max_length=50),
        ),
    ]
