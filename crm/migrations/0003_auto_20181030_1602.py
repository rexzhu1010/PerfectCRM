# Generated by Django 2.0.7 on 2018-10-30 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20181030_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': '缴费表', 'verbose_name_plural': '缴费表'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name_plural': '角色表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签', 'verbose_name_plural': '标签'},
        ),
    ]
