# Generated by Django 2.0.7 on 2018-12-04 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20181031_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='url_type',
            field=models.SmallIntegerField(choices=[(0, 'alias'), (1, 'absolute_url')], default=0),
        ),
        migrations.AlterField(
            model_name='customer',
            name='qq',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]