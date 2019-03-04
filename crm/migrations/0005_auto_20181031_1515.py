# Generated by Django 2.0.7 on 2018-10-31 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20181030_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '已报名'), (1, '未报名')], default=1),
        ),
    ]
