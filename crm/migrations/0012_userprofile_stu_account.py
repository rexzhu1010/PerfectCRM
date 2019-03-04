# Generated by Django 2.0.7 on 2018-12-19 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_auto_20181213_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stu_account',
            field=models.ForeignKey(blank=True, help_text='只有学员报名后方可为其创建帐号', null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='关联学员帐号'),
        ),
    ]
